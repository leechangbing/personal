import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType

# ========================
# 审核专用配置
# ========================
device = "mps" if torch.backends.mps.is_available() else "cpu"
model_name = "Qwen/Qwen3-8B"  # 或 Qwen/Qwen3-32B

tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    trust_remote_code=True,
    padding_side="left"  # 更适合生成任务（避免右填充干扰 EOS）
)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# 加载模型（MPS 兼容）
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map={"": device},
)
model.gradient_checkpointing_enable()

# LoRA 配置（针对审核任务，可适当降低秩）
peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False,
    r=4,                    # 审核任务相对简单，r=4 足够
    lora_alpha=8,
    lora_dropout=0.05,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
)

model = get_peft_model(model, peft_config)
model.print_trainable_parameters()

# ========================
# 审核专用数据预处理
# ========================
def formatting_prompts_func(example):
    """构建 SFT prompt：instruction + input -> output"""
    prompts = []
    for i in range(len(example['input'])):
        # 使用指令微调格式
        prompt = (
            "你是一名 TikTok 广告审核专家，请根据政策客观判断以下广告主是否存在风险。\n"
            "请严格按 JSON 格式输出：{\"isHit\": 0/1, \"Risk\": \"风险类别\", \"Reasons\": \"具体原因\"}\n\n"
            f"广告主信息：\n{example['input'][i]}\n\n"
            "审核结果："
        )
        prompts.append(prompt)
    return prompts

def tokenize_function(examples):
    # 构建完整输入：prompt + output
    full_texts = [
        prompt + output
        for prompt, output in zip(formatting_prompts_func(examples), examples['output'])
    ]
    return tokenizer(
        full_texts,
        truncation=True,
        max_length=1024,      # 审核上下文较长，建议 1024
        padding=False,
        add_special_tokens=True,
    )

# 加载 SFT 数据集（JSONL 格式）
dataset = load_dataset("json", data_files="tiktok_promote_risk_sft.jsonl")

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=["input", "output"],
    num_proc=4,
)

# ========================
# 审核专用训练参数
# ========================
training_args = TrainingArguments(
    output_dir="./qwen3-8b-tiktok-audit-sft",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    learning_rate=1e-4,               # 审核任务建议更低 LR
    num_train_epochs=2,               # 避免过拟合
    logging_steps=10,
    save_strategy="steps",
    save_steps=200,
    fp16=False,                       # MPS 必须关闭
    bf16=False,
    optim="adamw_torch",
    lr_scheduler_type="cosine",
    warmup_ratio=0.1,
    dataloader_pin_memory=False,
    remove_unused_columns=False,
    report_to="none",
    ignore_data_skip=True,
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
    pad_to_multiple_of=8,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    data_collator=data_collator,
    tokenizer=tokenizer,
)

trainer.train()
model.save_pretrained("./qwen3-8b-tiktok-audit-sft-final")
tokenizer.save_pretrained("./qwen3-8b-tiktok-audit-sft-final")
