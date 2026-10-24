import os
import json
import re
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    GenerationConfig
)
from peft import LoraConfig, PeftModel
import warnings

warnings.filterwarnings("ignore")

# 设置Mac环境变量优化（移除不兼容的MPS内存共享设置）
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # 避免Tokenizer并行警告

# --- 兼容性修复：检测并适配PyTorch版本 ---
torch_version = tuple(map(int, torch.__version__.split('.')[:2]))
print(f"PyTorch版本: {torch.__version__}")


# 安全的MPS初始化函数
def init_mps_support():
    """安全初始化MPS支持，兼容不同PyTorch版本"""
    try:
        if torch.backends.mps.is_available():
            # 只在PyTorch 2.1+版本启用内存共享
            if torch_version >= (2, 1):
                torch.backends.mps.enable_per_process_memory_sharing()
                print("✅ 启用MPS进程间内存共享")
            else:
                print("⚠️ PyTorch版本<2.1，跳过MPS内存共享设置")
            return True
        else:
            print("⚠️ MPS不可用，使用CPU训练")
            return False
    except Exception as e:
        print(f"⚠️ MPS初始化警告: {e}")
        return False


# 初始化MPS
is_apple_silicon = init_mps_support()

# --- 1. 数据准备 ---
sft_samples = [
    # 保持原有14个样本不变
    {
        "instruction": "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。",
        "input": "{\n  \"通用广告特征\": {\n    \"注册时长_天\": 0.1,\n    \"历史投放消耗_美元\": 0,\n    \"历史审核拒绝率\": 0.0\n  },\n  \"通用团伙特征\": {\n    \"是否命中团伙风险\": true,\n    \"团伙风险类型\": [\n      \"金融欺诈\",\n      \"杀猪盘\"\n    ],\n    \"邻居节点平均风险分\": 0.98\n  },\n  \"Promote用户\": {\n    \"粉丝数\": 1,\n    \"历史违规次数\": 0\n  },\n  \"Promote设备\": {\n    \"设备风险等级\": \"高\",\n    \"设备风险详情\": [\n      \"模拟器\"\n    ],\n    \"IP风险\": \"高风险IDC机房IP\"\n  }\n}",
        "output": "{\"isHit\": 1, \"Risk\": \"金融欺诈\", \"Reasons\": \"账户关联到'金融欺诈'和'杀猪盘'风险团伙，且设备环境为高风险模拟器和IDC机房IP，是典型的黑产欺诈行为。\"}"},
    {
        "instruction": "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。",
        "input": "{\n  \"通用广告特征\": {\n    \"注册时长_天\": 450,\n    \"历史投放消耗_美元\": 8000,\n    \"历史审核拒绝率\": 0.65\n  },\n  \"通用团伙特征\": {\n    \"是否命中团伙风险\": true,\n    \"团伙风险类型\": [\n      \"系统规避\"\n    ],\n    \"邻居节点平均风险分\": 0.75\n  },\n  \"Promote用户\": {\n    \"粉丝数\": 5600,\n    \"历史违规次数\": 25\n  },\n  \"Promote设备\": {\n    \"设备风险等级\": \"低\",\n    \"设备风险详情\": [],\n    \"IP风险\": \"正常\"\n  }\n}",
        "output": "{\"isHit\": 1, \"Risk\": \"系统规避\", \"Reasons\": \"账户历史审核拒绝率高达65%，且关联到'系统规避'团伙，表现出长期、反复尝试绕过平台审核策略的行为。\"}"},
    {
        "instruction": "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。",
        "input": "{\n  \"通用广告特征\": {\n    \"注册时长_天\": 1024,\n    \"历史投放消耗_美元\": 500000,\n    \"历史审核拒绝率\": 0.02\n  },\n  \"通用团伙特征\": {\n    \"是否命中团伙风险\": false,\n    \"团伙风险类型\": [],\n    \"邻居节点平均风险分\": 0.03\n  },\n  \"Promote用户\": {\n    \"粉丝数\": 2100000,\n    \"历史违规次数\": 1\n  },\n  \"Promote设备\": {\n    \"设备风险等级\": \"低\",\n    \"设备风险详情\": [],\n    \"IP风险\": \"正常\"\n  }\n}",
        "output": "{\"isHit\": 0, \"Risk\": \"无风险\", \"Reasons\": \"账户为长期活跃的高信誉品牌客户，各项指标均表现优秀，未发现任何风险证据。\"}"},
    {
        "instruction": "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。",
        "input": "{\n  \"通用广告特征\": {\n    \"注册时长_天\": 15,\n    \"历史投放消耗_美元\": 150,\n    \"历史审核拒绝率\": 0.1\n  },\n  \"通用团伙特征\": {\n    \"是否命中团伙风险\": false,\n    \"团伙风险类型\": [],\n    \"邻居节点平均风险分\": 0.88\n  },\n  \"Promote用户\": {\n    \"粉丝数\": 300,\n    \"历史违规次数\": 0\n  },\n  \"Promote设备\": {\n    \"设备风险等级\": \"低\",\n    \"设备风险详情\": [],\n    \"IP风险\": \"正常\"\n  }\n}",
        "output": "{\"isHit\": 1, \"Risk\": \"冒充\", \"Reasons\": \"尽管账户和设备特征正常，但其邻居节点平均风险分高达0.88，表明其与大量已知风险账户（如冒充、欺诈）存在紧密关联，存在极高的冒充他人或品牌的风险。\"}"},
    {
        "instruction": "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。",
        "input": "{\n  \"通用广告特征\": {\n    \"注册时长_天\": 30,\n    \"历史投放消耗_美元\": 200,\n    \"历史审核拒绝率\": 0.05\n  },\n  \"通用团伙特征\": {\n    \"是否命中团伙风险\": true,\n    \"团伙风险类型\": [\n      \"杀猪盘\"\n    ],\n    \"邻居节点平均风险分\": 0.91\n  },\n  \"Promote用户\": {\n    \"粉丝数\": 500,\n    \"历史违规次数\": 0\n  },\n  \"Promote设备\": {\n    \"设备风险等级\": \"中\",\n    \"设备风险详情\": [\n      \"VPN使用\"\n    ],\n    \"IP风险\": \"正常\"\n  }\n}",
        "output": "{\"isHit\": 1, \"Risk\": \"杀猪盘\", \"Reasons\": \"账户明确关联到'杀猪盘'风险团伙，这是高风险的欺诈行为，尽管其他账户特征不突出，但团伙证据是决定性的。\"}"},
    {
        "instruction": "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。",
        "input": "{\n  \"通用广告特征\": {\n    \"注册时长_天\": 5,\n    \"历史投放消耗_美元\": 50,\n    \"历史审核拒绝率\": 0.0\n  },\n  \"通用团伙特征\": {\n    \"是否命中团伙风险\": true,\n    \"团伙风险类型\": [\n      \"非法赌博\"\n    ],\n    \"邻居节点平均风险分\": 0.85\n  },\n  \"Promote用户\": {\n    \"粉丝数\": 88,\n    \"历史违规次数\": 0\n  },\n  \"Promote设备\": {\n    \"设备风险等级\": \"低\",\n    \"设备风险详情\": [],\n    \"IP风险\": \"正常\"\n  }\n}",
        "output": "{\"isHit\": 1, \"Risk\": \"非法赌博\", \"Reasons\": \"账户关联到'非法赌博'风险团伙，即使账户是新的且设备正常，其推广内容也极有可能导向非法赌博网站。\"}"},
    {
        "instruction": "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。",
        "input": "{\n  \"通用广告特征\": {\n    \"注册时长_天\": 2,\n    \"历史投放消耗_美元\": 10,\n    \"历史审核拒绝率\": 0.0\n  },\n  \"通用团伙特征\": {\n    \"是否命中团伙风险\": false,\n    \"团伙风险类型\": [],\n    \"邻居节点平均风险分\": 0.6\n  },\n  \"Promote用户\": {\n    \"粉丝数\": 15,\n    \"历史违规次数\": 0\n  },\n  \"Promote设备\": {\n    \"设备风险等级\": \"高\",\n    \"设备风险详情\": [\n      \"模拟器\"\n    ],\n    \"IP风险\": \"高风险IDC机房IP\"\n  }\n}",
        "output": "{\"isHit\": 1, \"Risk\": \"就业诈骗\", \"Reasons\": \"新注册账号使用高风险的模拟器和IDC机房IP，这是批量操作的典型特征，常用于发布虚假招聘等就业诈骗信息。\"}"},
    {
        "instruction": "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。",
        "input": "{\n  \"通用广告特征\": {\n    \"注册时长_天\": 180,\n    \"历史投放消耗_美元\": 1200,\n    \"历史审核拒绝率\": 0.3\n  },\n  \"通用团伙特征\": {\n    \"是否命中团伙风险\": true,\n    \"团伙风险类型\": [\n      \"禁止行业-成人服务、娱乐（色情导流）\"\n    ],\n    \"邻居节点平均风险分\": 0.8\n  },\n  \"Promote用户\": {\n    \"粉丝数\": 3500,\n    \"历史违规次数\": 8\n  },\n  \"Promote设备\": {\n    \"设备风险等级\": \"低\",\n    \"设备风险详情\": [],\n    \"IP风险\": \"正常\"\n  }\n}",
        "output": "{\"isHit\": 1, \"Risk\": \"禁止行业-成人服务、娱乐（色情导流）\", \"Reasons\": \"账户关联到明确的'色情导流'风险团伙，且历史违规次数较多，表明其内容方向持续触碰禁止行业政策。\"}"},
    {
        "instruction": "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。",
        "input": "{\n  \"通用广告特征\": {\n    \"注册时长_天\": 400,\n    \"历史投放消耗_美元\": 5000,\n    \"历史审核拒绝率\": 0.05\n  },\n  \"通用团伙特征\": {\n    \"是否命中团伙风险\": true,\n    \"团伙风险类型\": [\n      \"自杀与自残\"\n    ],\n    \"邻居节点平均风险分\": 0.9\n  },\n  \"Promote用户\": {\n    \"粉丝数\": 15000,\n    \"历史违规次数\": 2\n  },\n  \"Promote设备\": {\n    \"设备风险等级\": \"低\",\n    \"设备风险详情\": [],\n    \"IP风险\": \"正常\"\n  }\n}",
        "output": "{\"isHit\": 1, \"Risk\": \"自杀与自残\", \"Reasons\": \"账户关联到'自杀与自残'红线风险团伙，无论账户本身画像如何，一旦触及红线内容，必须判定为高风险。\"}"},
    {
        "instruction": "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。",
        "input": "{\n  \"通用广告特征\": {\n    \"注册时长_天\": 90,\n    \"历史投放消耗_美元\": 300,\n    \"历史审核拒绝率\": 0.0\n  },\n  \"通用团伙特征\": {\n    \"是否命中团伙风险\": false,\n    \"团伙风险类型\": [],\n    \"邻居节点平均风险分\": 0.1\n  },\n  \"Promote用户\": {\n    \"粉丝数\": 8000,\n    \"历史违规次数\": 0\n  },\n  \"Promote设备\": {\n    \"设备风险等级\": \"低\",\n    \"设备风险详情\": [],\n    \"IP风险\": \"正常\"\n  }\n}",
        "output": "{\"isHit\": 0, \"Risk\": \"无风险\", \"Reasons\": \"账户为健康成长的新晋创作者，粉丝增长良好，无任何不良行为记录，所有指标均正常。\"}"},
    {
        "instruction": "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。",
        "input": "{\n  \"通用广告特征\": {\n    \"注册时长_天\": 500,\n    \"历史投放消耗_美元\": 15000,\n    \"历史审核拒绝率\": 0.03\n  },\n  \"通用团伙特征\": {\n    \"是否命中团伙风险\": false,\n    \"团伙风险类型\": [],\n    \"邻居节点平均风险分\": 0.08\n  },\n  \"Promote用户\": {\n    \"粉丝数\": 50000,\n    \"历史违规次数\": 3\n  },\n  \"Promote设备\": {\n    \"设备风险等级\": \"低\",\n    \"设备风险详情\": [],\n    \"IP风险\": \"正常\"\n  }\n}",
        "output": "{\"isHit\": 0, \"Risk\": \"无风险\", \"Reasons\": \"账户为稳定的中小型商家，投放历史悠久，信誉良好，极低的拒审率和违规次数在正常范围内。\"}"},
    {
        "instruction": "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。",
        "input": "{\n  \"通用广告特征\": {\n    \"注册时长_天\": 250,\n    \"历史投放消耗_美元\": 50,\n    \"历史审核拒绝率\": 0.0\n  },\n  \"通用团伙特征\": {\n    \"是否命中团伙风险\": false,\n    \"团伙风险类型\": [],\n    \"邻居节点平均风险分\": 0.15\n  },\n  \"Promote用户\": {\n    \"粉丝数\": 950,\n    \"历史违规次数\": 0\n  },\n  \"Promote设备\": {\n    \"设备风险等级\": \"低\",\n    \"设备风险详情\": [],\n    \"IP风险\": \"正常\"\n  }\n}",
        "output": "{\"isHit\": 0, \"Risk\": \"无风险\", \"Reasons\": \"账户为个人生活分享者，投放消耗低，无商业意图，所有行为均符合普通用户的正常模式。\"}"},
    {
        "instruction": "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。",
        "input": "{\n  \"通用广告特征\": {\n    \"注册时长_天\": 800,\n    \"历史投放消耗_美元\": 80000,\n    \"历史审核拒绝率\": 0.01\n  },\n  \"通用团伙特征\": {\n    \"是否命中团伙风险\": false,\n    \"团伙风险类型\": [],\n    \"邻居节点平均风险分\": 0.06\n  },\n  \"Promote用户\": {\n    \"粉丝数\": 800000,\n    \"历史违规次数\": 1\n  },\n  \"Promote设备\": {\n    \"设备风险等级\": \"低\",\n    \"设备风险详情\": [],\n    \"IP风险\": \"正常\"\n  }\n}",
        "output": "{\"isHit\": 0, \"Risk\": \"无风险\", \"Reasons\": \"账户为垂直领域有影响力的专家，信誉记录优秀，投放行为专业且合规。\"}"},
    {
        "instruction": "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。",
        "input": "{\n  \"通用广告特征\": {\n    \"注册时长_天\": 1500,\n    \"历史投放消耗_美元\": 2000000,\n    \"历史审核拒绝率\": 0.001\n  },\n  \"通用团伙特征\": {\n    \"是否命中团伙风险\": false,\n    \"团伙风险类型\": [],\n    \"邻居节点平均风险分\": 0.01\n  },\n  \"Promote用户\": {\n    \"粉丝数\": 15000000,\n    \"历史违规次数\": 0\n  },\n  \"Promote设备\": {\n    \"设备风险等级\": \"低\",\n    \"设备风险详情\": [],\n    \"IP风险\": \"正常\"\n  }\n}",
        "output": "{\"isHit\": 0, \"Risk\": \"无风险\", \"Reasons\": \"账户为大型企业官方认证账号，具有极高的信誉和庞大的消耗，是平台的标杆性安全用户。\"}"}
]

# 将样本转换为Hugging Face Dataset对象
train_dataset = Dataset.from_list(sft_samples)

# --- 2. Mac专属配置 ---
base_model_name = "Qwen/Qwen3-8B-Instruct"
output_dir = "./qwen3-8b-promote-sft"
os.makedirs(output_dir, exist_ok=True)

print(f"检测到Apple Silicon: {is_apple_silicon}")
print(f"系统内存: 48GB")

# --- 3. 优化的模型加载配置 (适配Mac) ---
print("正在加载模型和Tokenizer...")

# Mac下优化的模型加载参数
model_kwargs = {
    "trust_remote_code": True,
    "torch_dtype": torch.float16 if is_apple_silicon else torch.float32,
    "device_map": "auto",
    "low_cpu_mem_usage": True,
    "attn_implementation": "eager",  # Mac不支持FlashAttention
}

# 加载模型（适配Mac的内存优化）
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    **model_kwargs
)

# 基础模型配置
base_model.config.use_cache = False
base_model.config.pretraining_tp = 1

# 移动到MPS设备（Apple Silicon）
if is_apple_silicon:
    try:
        base_model = base_model.to("mps")
        print("✅ 模型已移至MPS设备")
    except Exception as e:
        print(f"⚠️ 无法移动模型到MPS: {e}")
        print("ℹ️ 退回到CPU训练")

# 加载Tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    base_model_name,
    trust_remote_code=True,
    padding_side="right",
    use_fast=False,
    cache_dir=os.path.expanduser("~/.cache/huggingface/hub")  # Mac默认缓存目录
)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.pad_token_id = tokenizer.eos_token_id
tokenizer.padding_side = "right"


# --- 4. 数据处理函数 ---
def format_chat_template(example):
    messages = [
        {"role": "system", "content": "你是一名Tiktok Promote广告审核专家，严格按照要求输出JSON格式的审核结果。"},
        {"role": "user", "content": f"{example['instruction']}\n\n{example['input']}"},
        {"role": "assistant", "content": example['output']}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=False,
        padding=False
    )
    return {"text": text}


# 应用格式化（优化批处理）
formatted_dataset = train_dataset.map(
    format_chat_template,
    remove_columns=["instruction", "input", "output"],
    batched=True,  # 批处理加速
    batch_size=8
)

# --- 5. Mac优化的LoRA和训练参数 ---
# 轻量化LoRA配置（适配Mac内存）
lora_config = LoraConfig(
    r=32,  # 降低秩以减少内存占用
    lora_alpha=64,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    inference_mode=False,
)

# Mac专属训练参数（最大化利用48GB内存）
training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=2 if is_apple_silicon else 1,  # MPS可用时提升批次
    gradient_accumulation_steps=4,
    learning_rate=1e-4,
    num_train_epochs=6,
    logging_steps=1,
    save_strategy="epoch",
    save_total_limit=2,
    fp16=is_apple_silicon,  # 仅在MPS可用时启用FP16
    bf16=False,  # Mac不支持BF16
    optim="adamw_torch",  # 改用原生PyTorch优化器（Mac兼容）
    lr_scheduler_type="cosine",
    warmup_ratio=0.1,
    weight_decay=0.01,
    max_grad_norm=1.0,
    report_to="none",
    seed=42,
    disable_tqdm=False,
    dataloader_pin_memory=False,  # Mac关闭pin_memory提升性能
    dataloader_num_workers=0,  # Mac设置为0避免多线程问题
    gradient_checkpointing=True,  # 梯度检查点节省内存
)

# --- 6. 初始化SFTTrainer (Mac适配) ---
trainer = SFTTrainer(
    model=base_model,
    train_dataset=formatted_dataset,
    peft_config=lora_config,
    dataset_text_field="text",
    max_seq_length=1536,  # 适度降低序列长度平衡性能和内存
    tokenizer=tokenizer,
    args=training_args,
    packing=False,
    neftune_noise_alpha=5.0,
)

print("--- 开始SFT训练 (Mac优化版) ---")
trainer.train()
print("--- SFT训练完成 ---")

# --- 7. 保存模型 ---
final_model_path = os.path.join(output_dir, "final_checkpoint")
trainer.save_model(final_model_path)
print(f"LoRA适配器已保存至: {final_model_path}")
trainer.state.save_to_json(os.path.join(output_dir, "trainer_state.json"))


# --- 8. Mac优化的推理函数 ---
def run_inference(actor_doc_json_str):
    """Mac下优化的推理函数"""
    print("\n--- 开始推理测试 (Mac优化版) ---")

    # 加载微调后的模型
    model = PeftModel.from_pretrained(base_model, final_model_path)
    model.eval()

    # 移动到MPS设备
    if is_apple_silicon:
        try:
            model = model.to("mps")
        except Exception as e:
            print(f"⚠️ 推理时无法使用MPS: {e}")

    # 构建prompt
    instruction = "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。"

    messages = [
        {"role": "system",
         "content": "你是一名Tiktok Promote广告审核专家，严格按照要求输出JSON格式的审核结果，只输出JSON内容，不要添加任何额外文字。"},
        {"role": "user", "content": f"{instruction}\n\n{actor_doc_json_str}"}
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # Mac优化的生成配置
    gen_config = GenerationConfig(
        temperature=0.01,
        top_p=0.95,
        top_k=50,
        num_beams=2,  # 降低束搜索数量适配Mac
        max_new_tokens=300,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
        repetition_penalty=1.1,
        do_sample=False,
    )

    # Mac下的推理优化
    with torch.no_grad():
        inputs = tokenizer(prompt, return_tensors="pt")
        if is_apple_silicon:
            try:
                inputs = inputs.to("mps")
            except:
                pass

        # 内存优化：分块处理
        outputs = model.generate(
            **inputs,
            generation_config=gen_config,
            use_cache=True,  # 推理时启用缓存加速
        )

    # 提取输出
    response = tokenizer.decode(outputs[0][len(inputs.input_ids[0]):], skip_special_tokens=True).strip()

    # 清理JSON输出
    json_pattern = r'\{[\s\S]*\}'
    json_match = re.search(json_pattern, response)
    clean_response = json_match.group(0) if json_match else response

    print("输入的ActorDoc:")
    print(actor_doc_json_str)
    print("\n模型输出:")
    print(clean_response)

    # 验证JSON
    try:
        parsed_json = json.loads(clean_response)
        print("\n✅ JSON解析成功!")
        return parsed_json
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON解析失败: {e}")
        return None


# --- 9. 运行推理测试 ---
test_actor_doc = {
    "通用广告特征": {
        "注册时长_天": 0.5,
        "历史投放消耗_美元": 2,
        "历史审核拒绝率": 0.0
    },
    "通用团伙特征": {
        "是否命中团伙风险": True,
        "团伙风险类型": ["金融欺诈"],
        "邻居节点平均风险分": 0.99
    },
    "Promote用户": {
        "粉丝数": 0,
        "历史违规次数": 0
    },
    "Promote设备": {
        "设备风险等级": "高",
        "设备风险详情": ["模拟器", "代理IP"],
        "IP风险": "高风险IDC机房IP"
    }
}

# 运行推理
result = run_inference(json.dumps(test_actor_doc, indent=2, ensure_ascii=False))

# 打印结果
if result:
    print("\n📊 审核结果:")
    print(f"是否命中风险: {'是' if result['isHit'] == 1 else '否'}")
    print(f"风险类型: {result['Risk']}")
    print(f"风险原因: {result['Reasons']}")

# --- Mac内存清理 ---
import gc

gc.collect()
if is_apple_silicon:
    try:
        torch.mps.empty_cache()
    except:
        pass
print("\n✅ 内存已清理完成")