from openai import OpenAI

# 定义客户端
client = OpenAI(
    api_key='sk-bc075c74dc904554804d9d4c3331a49b',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 文本embd测试
def test_embd():
    model = 'text-embedding-v4'
    input_texts = '衣服的质量杠杠的'
    completion = client.embeddings.create(
        model=model,
        input=input_texts
    )
    text_embed = completion.data[0].embedding
    print(type(text_embed), len(text_embed))
    print(text_embed)


if __name__ == "__main__":
    test_embd() # 调用文本嵌入模型