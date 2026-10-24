import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ["DASHSCOPE_API_KEY"] = "sk-bc075c74dc904554804d9d4c3331a49b"

import torch
from sentence_transformers import SentenceTransformer

# 设备配置，MPS加速嵌入模型
device = "mps" if torch.backends.mps.is_built() else "cpu"
print(f"使用设备: {device}")

# 加载模型
print("正在加载文本向量化模型")
model = SentenceTransformer(
    model_name_or_path="BAAI/bge-small-zh-v1.5", # 指定模型名称
    cache_folder="./models",  # 指定本地缓存路径
    trust_remote_code=True
).to(device)

# 测试编码
embeddings = model.encode(["这是一个测试句子", "民法典规定"])
print(f"✅ 模型加载成功，测试文本向量形状: {embeddings.shape}")
