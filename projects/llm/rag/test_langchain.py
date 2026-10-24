import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ["DASHSCOPE_API_KEY"] = "sk-bc075c74dc904554804d9d4c3331a49b"

from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 定义工具 (使用tool修饰器)
@tool
def multiply(a: int, b: int) -> int:
    """将两个整数相乘"""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """将两个整数相加"""
    return a + b


if __name__ == "__main__":
    # 定义工具
    tools = [multiply, add]

    # 初始化模型
    model = ChatTongyi(model_name="qwen-max").bind_tools(tools)
    print(model)

    # 构建prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个强大的数学助手，可以使用工具解决问题。"),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),  # 必须包含！用于记录工具调用过程
        ]
    )

    # 创建agent
    agent = create_agent(model=model, tools=tools, system_prompt='你是一个强大的数学助手，可以使用工具解决问题')

    # 调用agent
    result = agent.invoke({
        "messages": [{"role": "user", "content": "123 乘以 456 再加上 789 等于多少？仅输出结果"}]
    })

    # 打印结果
    print(result)
    print(type(result))
    print(result.keys())
    print(type(result['messages']))
    for i in range(len(result['messages'])):
        msg = result['messages'][i]
        print(msg)
        print(type(msg))
    print(result['messages'][-1].content)
    print(result['messages'][-1].response_metadata)


