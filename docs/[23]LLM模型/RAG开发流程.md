1. Agent介绍
1.1 组件&架构
- 基本组件：
  - 推理能力->LLM：基本依赖LLM擅长对文本（或者将多模态数据对齐到文本语义空间，例如gui agent）进行处理或者推理
  - 任务定义->Prompt：用户会预设完成agent某个任务详细规划及步骤（sysstem prompt），以及用户输入的文本（user prompt）
  - 服务调度->MCP：另外结合可以提供function call的列表，包括功能描述description、函数签名，例如说搜多引擎查询接口、搜索keyword字符串，这些工具函数可以本地代码函数、新拉起进程函数、远程api，统一MCP化，MCP提供了函数签名注册列表，类似于服务注册发现；
  - 上下文信息->context：将这些拼接成为一个字符串组成上下文，
    - LLM根据上下文去推理决策应该调用哪个函数以及函数的详细参数，执行后再将函数返回结果拼接到上下文；
    - 经过多轮迭代，大模型会根据上下文信息决定是否完成了任务，或者超过最大迭代次数；
- Agent架构：
  - 单agent：单一上下文来存储执行过程中所有文本，很容易超过大模型的上下文长度（大模型采用多阶段不同文本长度预料进行训练，预训练预料4k居多，一般128k/256k文本预料进行sft/rl，拓展其文本处理能力，同时会用yarn进行上下文窗口scale，这种长度文本训练成本特别高，attention计算量是seq的平方，所以业界用sparse/linear attention进行优化），一旦超过大模型容易乱说话，所以现在大家追求llm场上下文处理能力，1m上下文可能是标配；
  - Workflow：通过langgraph/langchian将多个agent编排一个dag完成特定任务，比如像deepflow、owl、manus，不完全靠agent自主规划协调；
  - 多agent：将上下文按照功能拆分到多个agent中，比如root agent进行规划、协调，子agent进行特定领域任务执行，可以支持更长的上下文，然后子agent能够专注于处理好自己的任务，但问题是在实际任务协作过程中，分工协作需要子团队沟通确认，但多agent对于这块处理还不够，所以多agent在有些case中未必能够处理好。多agent实现方式有OpenAI handsoff机制，单进程本地代码实现，还有google a2a架构（agent注册发现，子agent以单独的进程部署到不同节点上，走a2a协议进程数据交互）。
  - Agent RL：当前agent，比如deepresearch，需要优化system prompt来完善效果，通过RL可以将规划、拆解任务、工具算下额能力内置到模型中，让模型更通用，业界比如openai、kimi、qwen deepresearch在做这块，相当于模型通过RL内置了端到端能力。
  - 其它：agent工具自主选择，可以通过rag/llm推理结合query来自主选择那些tool加入到function all集合里；多agent自主选择，如何选择子agent完成特定任务。
1.2 常见问题
1. 幻觉如何解决？从两方面入手，信息和任务
  1. 信息：提供更完整的上下文信息，包括知识图谱(knowledge graph, KG)+检索增强生成(Retrieval-Augmented Generation, RAG)，底层由图数据库和向量数据库支持。
  2. 任务：在任务描述增加约束，prompt： task + constraints
2. agent多模态使用：
  1. 如何组织数据：context
  2. 如何写提示词：prompt
  3. 如何做后训练：SFT

2. RAG介绍
2.1 LangChain
LangChain 是一个开源框架，旨在简化大语言模型（如 GPT、Llama、Claude 等）与外部数据、工具和逻辑的集成，从而构建更强大、更智能的应用。
名义含义：
- “Lang” = Language（语言）：指的是 大语言模型（Large Language Models, LLMs），如 GPT、Llama、Claude 等，强调该框架围绕语言模型构建应用。
- “Chain” = 链、链条：指的是将多个组件（如提示词、模型调用、外部工具、数据检索、后处理等）像链条一样串联起来，形成一个可执行的工作流。例如：用户输入 → 检索文档 → 构造提示 → 调用 LLM → 格式化输出，这一连串步骤就是一个 “Chain”。
- LangChain = Language（语言模型） + Chain（链式工作流），寓意通过组合和串联，释放大语言模型在真实场景中的潜力。
核心功能包括：
- 链（Chains）：将多个步骤（如提示词 + LLM 调用 + 后处理）组合成可复用的工作流。
- 检索增强生成（RAG）：让 LLM 能基于你的私有文档（如 PDF、数据库）回答问题。
- 工具集成：连接搜索引擎、计算器、API 等外部工具（例如通过“Agent”调用）。
- 记忆（Memory）：在对话中保留上下文（如聊天历史）。
- 支持多种 LLM 和向量数据库：兼容 OpenAI、Anthropic、Ollama、Hugging Face 等。
✅ 简单说：LangChain 是帮你“把大模型变成有用应用”的工具箱。 
2.2 LangGraph
LangGraph 是 LangChain 团队推出的一个用于构建“有状态、多参与者、循环逻辑”的 LLM 应用的库，特别适合构建 Agent（智能体）系统。
名字含义：
- “Lang” = Language（语言模型）：与 LangChain 一致，“Lang” 指的是 大语言模型（LLMs），如 GPT、Llama、Claude 等，表明该工具是为 基于语言模型的智能应用 而设计的。
- “Graph” = 图（有向图 / 状态图）：在这里指的是计算图（computation graph）或状态机图（state machine graph），即用节点（nodes）和边（edges）来表示程序逻辑。与 LangChain 中线性的 “Chain” 不同，Graph 支持：
  - 分支（条件判断）
  - 循环（反复思考、工具调用）
  - 多路径执行（多个 Agent 并行或协作）
  - 状态保持（在整个流程中维护和更新共享状态）
- LangGraph = Language（语言模型） + Graph（图状流程），寓意用图结构解锁语言模型在复杂推理和智能体系统中的潜力。
为什么需要 LangGraph？传统的链式（linear）流程无法处理：
- 多个 AI Agent 之间的协作
- 需要循环判断（如“继续思考”还是“输出答案”）
- 动态控制流（例如根据 LLM 输出决定下一步做什么）
LangGraph 的特点：
- 基于 有向图（Directed Graph） 模型定义应用逻辑，包含
- 每个节点可以是一个 LLM 调用、工具调用或函数。
- 支持状态（State）管理和循环（Cycles） —— 这是构建高级 Agent（如 ReAct、Plan-and-Execute）的关键。
- 构建“自主推理”系统，例如：一个 Agent 分析问题 → 调用工具 → 评估结果 → 决定是否继续
✅ 简单说：LangGraph 是 LangChain 的“升级版”，专门用来构建能思考、能循环、能协作的智能体（Agent）系统。 
两者关系：
- LangGraph 是 LangChain 生态的一部分，构建在 LangChain 之上。
- 如果你只需要线性流程（如“查文档 → 回答问题”），用 LangChain 就够了。
- 如果你需要构建能自我反思、多步决策、多 Agent 协作的复杂系统，就需要 LangGraph。

3. Langchain案例
3.1 工具调用-数学计算





3.2 文本RAG-民法典
3.2.1 基本流程
- 目标：基于民法典全文开发一个智能法律助手，根据用户输入问题索引法律条文，并根据引用数据回答用户问题。
- 流程：
  - 输入：query，即user_question
  - 检索：doc_chunk，即vectior_db
  - 调用：基于prompt将query和doc_chun组合成contex，调用llm；
  - 输出：解析llm输出的message
- 组件：
  - 嵌入模型：将text转化为embedding
  - 向量数据库：支持embedding的存储和查询
    - 语料：将doc分割为chunk之后，转化为embedding存储到向量数据库；
    - 查询：将query转化为embedding，在向量数据库中进行查询；
  - 智能体：输入user_question和检索语料，输出answer
    - llm：通过dashboard调用qwen-max
    - context：基于prompt模板将query和检索语料组合为context
    - langchain：基于langchain构建调度流程
  - 交互界面：基于gradio提供前端界面用于用户交互，包含输入框和输出框；
3.2.2 测试效果
1. 启动流程
[图片]
2. 交互界面
[图片]
3.2.3 实验代码
1. 安装环境

conda create --name agent python=3.10

# 基础库
conda install numpy pandas matplotlib seaborn jupyter scikit-learn pip tqdm requests pillow -c conda-forge -y

# Pytorch
conda install pytorch torchvision torchaudio -c pytorch -y 

# Tensofflow
conda install tensorflow tensorboard tf-keras -c apple -y

# Hugging Face
conda install transformers sentence_transformers datasets accelerate -c conda-forge -y

# Langchain 
conda install langchain langgraph langchain-core langchain-community langchain-huggingface langchain-chroma -c conda-forge -y

# Dashscope
conda install dashscope -c conda-forge -y

2. 任务代码
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ["DASHSCOPE_API_KEY"] = "sk-bc075c74dc904554804d9d4c3331a49b"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import torch
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.chat_models import ChatTongyi

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

import gradio as gr
import warnings
warnings.filterwarnings("ignore")

# 超参配置
API_KEY = 'sk-bc075c74dc904554804d9d4c3331a49b'
DOC_PATH = "civil_code.txt"
CACHE_PATH = "./models"
CHROMA_DB_PATH = "./chroma_db"  # 向量数据库保存目录
LLM_MODEL_NAME = "qwen-max"  # 百炼平台模型
EMBEDDING_MODEL_NAME = "BAAI/bge-small-zh-v1.5" #文本向量化模型


# 设备配置，MPS加速嵌入模型
device = "mps" if torch.backends.mps.is_built() else "cpu"
print(f"使用设备: {device}")


# 加载模型
print("正在下载嵌入模型...")
model = SentenceTransformer(
    model_name_or_path="BAAI/bge-small-zh-v1.5", # 指定模型名称
    cache_folder="./models",  # 指定本地缓存路径
    trust_remote_code=True
).to(device)
embeddings = model.encode(["这是一个测试句子", "民法典规定"])
print(f"✅ 模型下载成功，测试文本向量形状: {embeddings.shape}")


# 分割文档
def load_and_split_documents(doc_path):
    if not os.path.exists(doc_path):
        raise FileNotFoundError(f"未找到文件：{doc_path}")

    loader = TextLoader(doc_path, encoding="utf-8")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=64,
        separators=["\n\n", "。\n", "\n", "。", "；", "？", "！", " ", ""]
    )
    split_docs = text_splitter.split_documents(documents)
    print(f"✅ 共分割出 {len(split_docs)} 个文本块")
    return split_docs


# 初始化嵌入模型
def get_embedding_model():
    model_kwargs = {"device": device}
    encode_kwargs = {"normalize_embeddings": True}

    # 加载现有嵌入模型
    print("📂 加载嵌入模型...")
    embeddings_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME, # 指定模型名称
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
    print("✅ 嵌入模型加载成功")
    return embeddings_model


# 创建或加载chroma向量数据库
def create_or_load_chroma_db(doc_path, embedding_model, db_path):
    if not os.path.exists(db_path):
        print("🔍 正在创建 Chroma 向量数据库...")
        docs = load_and_split_documents(doc_path)

        # 使用 Chroma 保存，自动持久化
        chroma_db = Chroma.from_documents(
            documents=docs,
            embedding=embedding_model,
            persist_directory=db_path,
            collection_name="civil_code"
        )
        print("✅ 向量数据库创建并保存完成")
    else:
        print("📂 加载现有 Chroma 数据库...")
        chroma_db = Chroma(
            persist_directory=db_path,
            embedding_function=embedding_model,
            collection_name="civil_code"
        )
        print("✅ 向量数据库加载完成")
    return chroma_db


# 获取千问大模型
def get_qwen_llm():
    llm = ChatTongyi(
        model_name=LLM_MODEL_NAME,
        dashscope_api_key=API_KEY,
        temperature=0.3,
        top_p=0.9,
        max_tokens=1024,
    )
    return llm

# 自定义prompt模版
PROMPT_TEMPLATE = """
【任务角色】：你是一名专业、严谨的中国法律助手，请根据以下从《中华人民共和国民法典》中检索到的内容回答问题。
【检索条文】：{context}
【用户问题】：{question}
【回答要求】：
1. 回答应严格基于上述内容，不得编造或猜测；
2. 若信息不足，请回答：“依据现有资料无法确定，请咨询专业律师。”；
3. 使用通俗语言解释法律概念；
4. 必须注明所依据的具体条款（如“《民法典》第XXXX条”）；
5. 最后添加免责声明：“本回答仅供参考，不构成正式法律意见，建议咨询执业律师。”
"""

# 创建RAG chain
def create_rag_chain_with_sources(vector_db, llm, prompt):
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    answer_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    full_chain = RunnableParallel(
        answer=answer_chain,
        sources=retriever  # 此时 retriever 收到的是字符串
    )
    return full_chain


# 查询函数
def query_legal_assistant(rag_chain, question):
    try:
        result = rag_chain.invoke(input=question)
        answer = result["answer"].strip().replace('\n','')
        sources = result["sources"]
        citations_num = len(sources)
        citations_content = '\n'.join([doc.page_content[:100].strip().replace('\n','') + "..." for doc in sources]) if sources else "无具体条文匹配"
        return f"✅ 调用成功\n[回答]:\n{answer}\n[来源]:引用条文数量{citations_num}\n{citations_content}"
    except Exception as e:
        return f"❌ 调用失败：{str(e)}\n\n请检查网络连接或 API Key 是否正确。"


# 启动gradio web界面
def launch_gradio_interface(rag_chain):
    def respond(message, history):
        response = query_legal_assistant(rag_chain, message)
        return response

    demo = gr.ChatInterface(
        fn=respond,
        title="⚖️ 法律智能助手 - 基于《民法典》与 Qwen-Max (Chroma版)",
        description="输入您的法律问题，例如：\n• 房东不退押金怎么办？\n• 结婚彩礼能要回来吗？\n• 孩子玩游戏充值可以退款吗？",
        examples=[
            "租房押金不退合法吗？",
            "离婚时财产怎么分？",
            "借条没有写利息还能主张吗？",
            "楼上漏水导致我家受损，谁负责？"
        ],
        # retry_btn="🔄 重试",
        # undo_btn="↩️ 撤回",
        # clear_btn="🗑️ 清空"
    )
    demo.launch(server_name="0.0.0.0", server_port=7860)

# 数据测试
def rag_test():
    embedding_model = get_embedding_model()
    chroma_db = create_or_load_chroma_db(doc_path=DOC_PATH, embedding_model=embedding_model, db_path=CHROMA_DB_PATH)
    retriever = chroma_db.as_retriever()
    docs = retriever.invoke("继承从什么时间开始？")
    print("✅ 向量数据库测试成功，单独测试检索结果:", len(docs))

    llm_model = get_qwen_llm()
    PROMPT = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])
    rag_chain = create_rag_chain_with_sources(vector_db=chroma_db, llm=llm_model, prompt=PROMPT)
    result = rag_chain.invoke("继承从什么时候开始？")
    print(result)
    print("回答:", result["answer"].replace("\n", ""))
    print("来源:", [doc.page_content[:100] + "..." for doc in result["sources"]])
    print(f"✅ RAG-Chain测试成功")

    response = query_legal_assistant(rag_chain=rag_chain, question='继承从什么时间开始？')
    print(response)
    print(f"✅ 单词查询测试成功")


def launch_gradio_interactive_example():
    # 启动交互界面
    print("🚀 正在启动法律智能助手（Chroma 版）...")

    # 1. 加载嵌入模型（自动使用 MPS 加速）
    embeddings_model = get_embedding_model()

    # 2. 创建或加载 Chroma 数据库
    vector_db = create_or_load_chroma_db(DOC_PATH, embeddings_model, CHROMA_DB_PATH)

    # 3. 初始化 Qwen-Max 模型
    try:
        llm_model = get_qwen_llm()
        print("✅ 成功连接百炼平台 Qwen-Max 模型")
    except Exception as e:
        print(f"❌ 模型初始化失败：{e}")
        exit(1)

    # 4. 定义prompt模板
    PROMPT = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])

    # 5. 构建 RAG 链
    rag_chain = create_rag_chain_with_sources(vector_db, llm_model, PROMPT)
    print("🧠 RAG 系统构建完成！")

    # 6. 启动 Web 界面
    print("🌐 正在启动服务：http://localhost:7860")
    launch_gradio_interface(rag_chain)

# 主程序入口
if __name__ == "__main__":

    # 调用测试
    rag_test()

    # 正式启动
    launch_gradio_interactive_example()




