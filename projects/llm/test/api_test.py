import json
import base64
from pathlib import Path
from openai import OpenAI, AsyncOpenAI
import asyncio

# 定义客户端
client = OpenAI(
    api_key='sk-bc075c74dc904554804d9d4c3331a49b',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 输出格式解析
def response_output(completion, stream=False):
    reasoning_content = ''
    answer_content = ''
    usage_info = ''
    is_thinking = False
    is_answering = False

    if stream is False:
        usage_info = completion.usage
        answer_content = completion.choices[0].message.content
        print(completion.model_dump_json())
        print(f'\nAnswer:\n{answer_content}\nUasge:\n{usage_info}')
    else:    
        for chunk in completion:
            if not chunk.choices:
                usage_info = chunk.usage
                print('\nUsage:\n{}'.format(chunk.usage))
            else:
                delta = chunk.choices[0].delta
                if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
                    if is_thinking is False:
                        print("Think:")
                        is_thinking = True
                    print(delta.reasoning_content.replace('\n', ''), end='', flush=True)
                    reasoning_content += delta.reasoning_content.replace('\n', '')
                else:
                    if delta.content != "" and is_answering is False:
                        is_answering = True
                        print('\nAnswer:' if is_thinking is True else 'Answer:')
                    print(delta.content, end='', flush=True)
                    answer_content += delta.content
    return reasoning_content, answer_content, usage_info 

# 文本生成测试
def text_output_test():
    completion = client.chat.completions.create(
        model="deepseek-r1", #deepseek-r1, deepseek-v3, qwen-max, qwen-plus, qwq-32b
        messages=[
            {'role': 'system', 'content': '你是一名具有丰富教学经验的中学英语老师'},
            {'role': 'user', 'content': '你是谁？'}
        ],
    )
    response_output(completion)

# 流式输出测试
def text_stream_output_test():
    completion = client.chat.completions.create(
        model="qwq-32b",  #deepseek-r1, deepseek-v3, qwen-max, qwen-plus, qwq-32b
        messages=[
            {'role': 'system', 'content': '你是一名具有丰富教学经验的中学英语老师'},
            {'role': 'user', 'content': '你是谁？'}
        ],
        stream=True,
        stream_options={"include_usage": True},
    )
    response_output(completion, True)

# 格式化输出
def text_format_output_test():
    example_response = json.dumps(
        {
            '姓名': '张三',
            '职业': '英语老师'
        },
        ensure_ascii=False
    )

    completion = client.chat.completions.create(
        model="qwen-plus", #deepseek-r1, deepseek-v3, qwen-max, qwen-plus, qwq-32b
        messages=[
            {'role': 'system', 'content': f'提取姓名和职业, 输出包含姓名和职业的JSON. 示例: Q: 我叫张三，是一名英语老师, A:{example_response}'},
            {'role': 'user', 'content': '我叫李四，是一名外科手术医生'}
        ],
        response_format={"type": "json_object"},
    )

    response_output(completion)

# 文本理解测试
def text_summary_test():
    file_object = client.files.create(file=Path("使用笔记.md"), purpose="file-extract")
    completion = client.chat.completions.create(
        model="qwen3-max",
        messages=[
            {'role': 'system', 'content': f'fileid://{file_object.id}'},
            {'role': 'user', 'content': '请根据文章中内容，输出论文摘要，保证markdown格式.'}
        ],
        stream=True,
        stream_options={"include_usage": True},
    )
    response_output(completion, True)

# 图像理解测试
def image_summary_test():
    # 将图像转为Base64字符串，直接嵌入请求体
    with open("./data/dog_and_girl.jpeg", "rb") as image_file:
        base64_data = base64.b64encode(image_file.read()).decode('utf-8')
    image_url = f'data:image/jpeg;base64,{base64_data}'
    
    completion = client.chat.completions.create(
        model="qwen-vl-max",
        messages=[
            {"role": "user","content": [
                {"type": "text","text": "图中描述了什么信息，并总结"},
                {"type": "image_url",
                "image_url": {"url": f'{image_url}'}}
                ]
            }
        ],
        stream= True,
        stream_options={"include_usage": True},
    )
    response_output(completion, True)


# 异步调用功能
async def async_test():
    client = AsyncOpenAI(
        api_key='sk-bc075c74dc904554804d9d4c3331a49b',
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completions = await client.chat.completions.create(
        model="deepseek-v3",
        messages=[
            {"role": "system", "content": "你是一名经验丰富的中学数学老师"},
            {"role": "user", "content": "你是谁"}
        ]
    )
    response_output(completions, False)

# qwen3系列模型测试

def qwen3_test():
    completion = client.chat.completions.create(
        model="qwen3-32b", #qwen3-235b-a22b, qwen3-30b-a3b, qwen3-32b, qwen3-14b, qwen3-8b, qwen3-4b, qwen3-1.7b, qwen3-0.6b
        messages=[
            {'role': 'system', 'content': '你是一名具有丰富教学经验的中学英语老师'},
            {'role': 'user', 'content': '你是谁？'}
        ],
        stream=True,
        stream_options={"include_usage": True},
        extra_body={"enable_thinking": True},
        
    )
    response_output(completion, True)


if __name__ == '__main__':
    text_output_test()
    text_stream_output_test()
    text_format_output_test()
    text_summary_test()
    image_summary_test()
    asyncio.run(async_test())
    qwen3_test()