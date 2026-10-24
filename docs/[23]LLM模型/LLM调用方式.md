1. 本地部署
1.1  Ollama
链接：https://ollama.com/


1.2 Hugging Face
链接：https://huggingface.co/


2. API调用
2.1 SiliconCloud
- Base URL: https://api.siliconflow.cn/v1
- API key: sk-ojiiawzsrxaovlqwwezfmjfcrlcivxeqicsswksisdbpmdel
2.1.1 模型广场
https://cloud.siliconflow.cn/models
[图片]



2.2 Aliyun
- Base URL: 
- API Key: 
2.2.1 模型广场


3. 应用场景
3.1 Cline 
安装链接：
3.2 OpenManus
安装链接：https://github.com/mannaandpoem/OpenManus?tab=readme-ov-file#installation
# Global LLM configuration
[llm]
model = "Qwen/QwQ-32B" # 或者平台中的其他支持 function calling 模型，参见[Function Calling](https://docs.siliconflow.cn/cn/userguide/guides/function-calling)
base_url = "https://api.siliconflow.cn/v1"
api_key = "your_api_key_from_siliconcloud"
max_tokens = 16384
temperature = 0.6

# Optional configuration for specific LLM models
[llm.vision]
model = "Qwen/Qwen2-VL-72B-Instruct" # 或者平台中的其他视觉语言模型，参见[vision](https://docs.siliconflow.cn/cn/userguide/capabilities/vision)
base_url = "https://api.siliconflow.cn/v1"
api_key = "your_api_key_from_siliconcloud"
3.3 DeepResearch

3.4 Trace
连接：https://www.trae.com.cn/
介绍：AI IDE， 

4. MCP服务



