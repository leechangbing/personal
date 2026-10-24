import os
import json
from typing import List
from openai import AsyncOpenAI
import asyncio
import aiofiles  
from tqdm.asyncio import tqdm_asyncio

# 配置常量（集中管理参数）
MAX_CONCURRENT_TASKS = 100
MODEL_NAME = "qwen3-max"
INPUT_DIR = "data/position"
OUTPUT_DIR = "data/position_res"

client = AsyncOpenAI(
        api_key='sk-bc075c74dc904554804d9d4c3331a49b',
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

async def async_task_test(file_path: str, semaphore: asyncio.Semaphore) -> str:
    """异步处理单个文件的任务"""
    try:
        async with semaphore:  # 通过信号量控制并发
            # 异步读取文件
            async with aiofiles.open(file_path, 'r') as f:
                content = await f.read()
            # 构造prompt
            example_response = json.dumps({'x': '10', 'y': '10'}, ensure_ascii=False)
            system_prompt = f"提取坐标信息，输出包括x和y的JSON。示例: {example_response}"
            # 调用大模型API
            completions = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ],
                response_format={"type": "json_object"},
                timeout=300  # 增加超时控制
            )
            # 解析响应结果
            answer_content = completions.choices[0].message.content
            # 异步写入结果
            output_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_res.txt"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            async with aiofiles.open(output_path, 'w') as f_out:
                await f_out.write(answer_content)
            return answer_content
    except asyncio.TimeoutError:
        print(f"⏰ 超时: {file_path}")
        return ""
    except Exception as e:
        print(f"❌ 错误处理 {file_path}: {str(e)}")
        return ""

async def main(file_paths: List[str]):
    """主协程，管理所有任务"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
    tasks = [async_task_test(fp, semaphore) for fp in file_paths]
    results = await tqdm_asyncio.gather(*tasks, desc="处理进度")
    success_count = sum(1 for res in results if res)
    print(f"\n✅ 成功: {success_count} | ❌ 失败: {len(file_paths) - success_count}")

if __name__ == '__main__':
    file_list = [os.path.join(INPUT_DIR, f"{i:02d}.txt") for i in range(10)]
    asyncio.run(main(file_list))
