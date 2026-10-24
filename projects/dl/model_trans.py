import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

import torch
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification

if __name__ == "__main__":

    # 加载预训练模型和分词器
    model_name = "bert-base-uncased"
    # model_name = 'distilbert-base-uncased-finetuned-sst-2-english'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    print(model)

    # 进行文本编码
    text = "I love Hugging Face!"
    inputs = tokenizer(text, return_tensors="pt")  # "pt" 表示 PyTorch 张量
    print(inputs)

    # 模型推理
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=-1).item()
    print("Predicted class:", predicted_class)
