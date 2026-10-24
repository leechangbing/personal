import json
import torch
from datetime import datetime
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM

# 加载model和tokenizer
def load_model(model_name, device):
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,  # 使用 FP16 减少内存占用
        device_map="auto",  # 自动分配到 MPS
        trust_remote_code=True,
    )
    return tokenizer, model

# 加载数据
def load_data(train_data_path, test_data_path):
    dataset = load_dataset("csv", data_files={"train": train_data_path, "test": test_data_path})
    train_dataset = dataset["train"]
    test_dataset = dataset["test"]
    return train_dataset, test_dataset

# 生成内容
def gen_content(model, tokenizer, messages, device):
    # 输入消息进行编码
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    # 内容生成
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=5120,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    # 解码器
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response


if __name__ == "__main__":
    # 检查设备
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")

    # 加载数据
    train_dataset, test_dataset = load_data('test_data.csv', 'test_data.csv')
    prompt = json.dumps(train_dataset[0], ensure_ascii=False, indent=4)
    messages = [{"role": "user", "content": prompt}]

    # 模型加载
    print(f"时间：{datetime.now()}")
    model_name = "./Qwen/Qwen3-8B"  # 或本地路径
    tokenizer, model = load_model(model_name, device)
    print(f"时间：{datetime.now()}")

    # 输出结果
    response = gen_content(model, tokenizer, messages, device)
    print("Response:", response)
    print(f"时间：{datetime.now()}")


