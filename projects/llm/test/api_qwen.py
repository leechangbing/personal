import os
import json
import base64
from pathlib import Path
from openai import OpenAI, AsyncOpenAI
import asyncio
import platform

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
def text_output_test(model):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': '你是一名具有丰富教学经验的中学英语老师'},
            {'role': 'user', 'content': '你是谁？'}
        ],
    )
    response_output(completion)


# 流式输出测试
def text_stream_output_test(model):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': '你是一名具有丰富教学经验的中学英语老师'},
            {'role': 'user', 'content': '你是谁？'}
        ],
        stream=True,
        stream_options={"include_usage": True},
    )
    response_output(completion, True)


# 格式化输出
def text_format_output_test(model):
    example_response = json.dumps(
        {
            '姓名': '张三',
            '职业': '英语老师'
        },
        ensure_ascii=False
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system',
             'content': f'提取姓名和职业, 输出包含姓名和职业的JSON. 示例: Q: 我叫张三，是一名英语老师, A:{example_response}'},
            {'role': 'user', 'content': '我叫李四，是一名外科手术医生'}
        ],
        response_format={"type": "json_object"},
    )

    response_output(completion)


# 文本理解测试
def text_summary_test(model):
    file_object = client.files.create(file=Path("使用笔记.md"), purpose="file-extract")
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': f'fileid://{file_object.id}'},
            {'role': 'user', 'content': '请根据文章中内容，输出论文摘要，保证markdown格式.'}
        ],
        stream=True,
        stream_options={"include_usage": True},
    )
    response_output(completion, True)

# 异步调用功能
async def async_test(model):
    client = AsyncOpenAI(
        api_key='sk-bc075c74dc904554804d9d4c3331a49b',
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completions = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一名经验丰富的中学数学老师"},
            {"role": "user", "content": "你是谁"}
        ]
    )
    response_output(completions, False)


# qwen3系列模型测试

def qwen3_test():
    completion = client.chat.completions.create(
        model="qwen3-32b",
        # qwen3-235b-a22b, qwen3-30b-a3b, qwen3-32b, qwen3-14b, qwen3-8b, qwen3-4b, qwen3-1.7b, qwen3-0.6b
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
    model = "qwen3-max"
    text_output_test(model)
    # text_stream_output_test(model)
    # text_format_output_test(model)
    # text_summary_test(model)
    # image_summary_test(model)
    # asyncio.run(async_test(model))
    # qwen3_test(model)