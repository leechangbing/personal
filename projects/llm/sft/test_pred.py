import torch
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM

# 检查 MPS 是否可用
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

# 模型加载
print(f"时间：{datetime.now()}")
model_name = "Qwen/Qwen3-8B"  # 或本地路径
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # 使用 FP16 减少内存占用
    device_map="auto",          # 自动分配到 MPS
    trust_remote_code=True,
)
print(f"时间：{datetime.now()}")

# 模型输入
prompt = "请介绍一下人工智能的发展历史。"
messages = [{"role": "user", "content": prompt}]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(device)
print(f"时间：{datetime.now()}")

# 生成内容
generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512,
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
    pad_token_id=tokenizer.eos_token_id
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]
print(f"时间：{datetime.now()}")


# token解码
response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print("Response:", response)
print(f"时间：{datetime.now()}")
