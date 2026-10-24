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



