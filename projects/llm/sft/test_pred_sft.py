import json
import torch
from peft import PeftModel
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM

# 加载数据
def load_data(train_data_path, test_data_path):
    dataset = load_dataset("csv", data_files={"train": train_data_path, "test": test_data_path})
    return dataset

# promote模板
def formatting_prompts_func(example):
    output_texts = []
    for i in range(len(example['input'])):
        text = f"### Input:\n{example['input'][i]}\n\n### Response:\n{example['output'][i]}{tokenizer.eos_token}"
        output_texts.append(text)
    return output_texts

# token编码
def tokenize_function(examples):
    # 注意：不要在这里 return_tensors="pt"，Trainer 会自动处理
    return tokenizer(
        formatting_prompts_func(examples),
        truncation=True,
        max_length=5120,
        padding=False,  # 改为动态填充（由 DataCollator 处理）
        add_special_tokens=True,
    )


def load_model(base_model_name, lora_adapter_path, device):
    # === 1. 加载 tokenizer 和基础模型 ===
    tokenizer = AutoTokenizer.from_pretrained(
        base_model_name,
        trust_remote_code=True,
        padding_side="left"  # 推理时通常 left padding 更安全（但生成一般不 padding）
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16,
        trust_remote_code=True,
        device_map={"": device}
    )

    return tokenizer, model


# === 3. 构造 prompt（必须和训练时一致！）===
def build_prompt(instruction: str, input_text: str) -> str:
    # 注意：这里必须和训练时的 formatting_prompts_func 完全一致！
    return f"### Input:\n{input_text}\n\n### Response:\n"


# pred_prompt模板
def formatting_prompts_func_train(example):
    output_texts = []
    for i in range(len(example['input'])):
        text = f"""
            ### Instruction:\n{example['instruction'][i]}\n
            ### Input:\n{example['input'][i]}\n
            ### Response:\n{example['output'][i]}{tokenizer.eos_token}"""
        output_texts.append(text)
    return output_texts

# pred_prompt模板
def formatting_prompts_func_pred(example):
    output_texts = []
    for i in range(len(example['input'])):
        text = f"""
            ### Instruction:\n{example['instruction'][i]}\n
            ### Input:\n{example['input'][i]}{tokenizer.eos_token}"""
        output_texts.append(text)
    return output_texts

# token编码
def tokenize_function(examples):
    # 注意：不要在这里 return_tensors="pt"，Trainer 会自动处理
    return tokenizer(
        formatting_prompts_func(examples),
        truncation=True,
        max_length=512,
        padding=False,  # 改为动态填充（由 DataCollator 处理）
        add_special_tokens=True,
    )


# 推理函数
def generate_response(instruction: str, input_text: str, max_new_tokens=256):
    prompt = build_prompt(instruction, input_text)

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        add_special_tokens=True
    ).to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    # 解码生成结果
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # 提取 Response 之后的内容（可选）
    if "### Response:\n" in generated_text:
        response = generated_text.split("### Response:\n", 1)[1]
    else:
        response = generated_text[len(prompt):].strip()

    return response.strip()


# === 5. 使用示例 ===
if __name__ == "__main__":

    # 参数配置
    base_model_name = "Qwen/Qwen3-8B"
    lora_adapter_path = "./qwen3-8b-lora-sft-final"  # 你保存的 LoRA 路径
    device = "mps" if torch.backends.mps.is_available() else "cpu"

    # 加载模型，LoRA适配器，并切换到评估模式
    tokenizer, model = load_model(base_model_name, lora_adapter_path, device)
    model = PeftModel.from_pretrained(model, lora_adapter_path)
    model.eval()
    print("✅ 模型加载完成！")


    # 加载数据
    instruction = "你是一名Tiktok Promote广告审核专家。请根据以下广告主信息（ActorDoc），依据审核政策（Policy），判断该广告是否存在风险。你的输出必须是一个JSON对象，包含isHit, Risk, Reasons三个字段。"
    dataset = load_data("test_data.csv", "test_data.csv")
    input_text = dataset["train"][0]["input"]

    output = generate_response(instruction, input_text)
    print("Generated Output:", output)

    # 如果 output 是 JSON 字符串，可以解析
    try:
        parsed = json.loads(output)
        print("Parsed:", parsed)
    except json.JSONDecodeError:
        print("Output is not valid JSON.")
