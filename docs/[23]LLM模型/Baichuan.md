Github：https://github.com/baichuan-inc
Hugging face：https://huggingface.co/baichuan-inc
Arxiv：Baichuan 2: Open Large-scale Language Models
Baichuan-7B
介绍
Baichuan-7B是由百川智能开发的第一个开源可商用的大规模预训练语言模型。基于Transfromer结构，在大约1.2万亿tokens上训练的70亿参数模型，支持中英文双语，上下文窗口长度为4096。在标准的中文和英文benchmark（C-Eval/MMLU）上均取得同尺寸最好的效果。
Benchmark结果
中文评测
C-Eval数据集是一个全面的中文基础评测数据集，由13948个选择题组成，涵盖了52个学科和四个难度的级别。使用该数据集的dev数据集作为few-shot的来源，在test集上进行了5-shot测试。
暂时无法在飞书文档外展示此内容
英文测评
MMLU是包含57个多选任务的英文评测数据集，涵盖了初等数学、美国历史、计算机科学、法律等，难度覆盖高中水平到专家水平，是目前主流的LLM评测数据集。采用了开源的评测方法，并进行了5-shot测试。
暂时无法在飞书文档外展示此内容
推理
推理代码已经在官方Huggingface库
暂时无法在飞书文档外展示此内容
数据
- 原始数据包括开源的中英文数据和自行抓取的中文互联网数据，以及部分高质量知识性数据。
- 参考相关性工作，频率和质量是数据处理环节重点考虑的两个维度。我们基于启发式规则和质量模型打分，对原始数据集进行篇章和句子粒度的过滤。在全量数据上，利用局部敏感哈希方法，对篇章和句子粒度做滤重。
[图片]
- 经过不断地调整和多轮测试，最终确认了一个在下游任务上表现最好的中英文匹配。
- 使用了一个基于自动学习的数据权重策略，对不同类别的数据进行配比。
分词
参考学术界方案使用SentencePiece中的Byte-Pair Encoding (BPE)作为分词算法，并且进行了一下的优化：
- 目前大部分开源模型主要基于英文优化，因此对中文语料存在效率较低的问题。我们使用了2000万条以中英为主的多语言语料训练分词模型，显著提升了对于中文的压缩率。
- 对于数学领域，我们参考率LLaMA和Galactica中的方案，对数字的每一位单独分开，避免出现数字不一致的问题，对于提升数学能力有重要帮助。
- 对于罕见字词（如特殊符号等），支持UTF-8 characters的byte编码，因此做到未知字词的全覆盖。
- 分析了不同分词器对语料的压缩率，可见我们的分词器明显优于LLaMA，Falcon等开源模型，并且对比其他中文分词器在压缩率相当的情况下，训练和推理效率更高。
暂时无法在飞书文档外展示此内容
模型结构
整体模型基于标准的transformer结构，采用了LLaMA一样的模型设计：
- 位置编码：rotary-embedding是现阶段被大多模型采用的位置编码方案，具有更好的外延效果。虽然训练过程中最大长度为4096，但是实际测试过程中模型可以很好的扩展到5000tokens以上，如下图：
- 激活层：SwiGLU，Feedforward变化为8/3倍的隐含层大小，即11008
- Layer-Normalization：基于RMSNorm的Pre-Normalization
[图片]
训练稳定性和吞吐
在原本的LLaMA框架上进行诸多修改以提升训练时的吞吐，具体包括：
- 算子优化技术：采用更高效算子，如Flash-Attentiton, NVIDIA apex的RMSNorm等
- 算子切分技术：将部分计算算子进行切分，减少内存峰值
- 混合精度技术：降低在不损失模型精度的情况下加速计算过程
- 训练容灾技术：训练平台和训练框架联合优化，Iaas+PaaS实现分钟级的故障定位和任务恢复
- 通信优化技术：
  - 采用拓扑感知的集合通信算法，避免网络拥塞问题，提高通信效率；
  - 根据卡数自适应设置bucket size，提高带宽利用率；
  - 根据模型和集群环境，调优通信原语的触发时机，从而将计算和通信重叠；
基于上述的几个优化技术，我们在千卡A800显卡上达到了7B模型182TFLOPS的吞吐，GPU峰值利用率高达58.3%。
[图片]
训练方法
安装依赖
暂时无法在飞书文档外展示此内容
准备数据
用户将训练语料按总rank数的倍数均匀切分为多个UTF-8文本文件，放置在语料目录中（默认为data_dir）下。各个rank进程将会读取语料目录下的不同文件，全部加载到内存后，开始后续训练过程。以上是简化的示范流程，建议用户在正式训练任务中，根据需求调整数据生产逻辑。
下载tokenizer模型
下载tokenizer模型文件，tokenizer.model，放置在项目目录下。
配置DeepSpeed
本示范代码采用DeepSpeed框架进行训练。用户根据集群情况，修改config/hostfile，如果是多机多卡，需要修改ssh中各个节点的IP配置。具体可以参考DeepSpeed官方说明。
执行训练
暂时无法在飞书文档外展示此内容
Third-Party Resources
1. LLaMA Efficient Tuning支持Baichuan-7B使用Qlora进行Finerune，支持RLHF，支持WebDemo。使用经过sft的模型见Baichuan-7B-sft。
2. fireballon/baichuan-vicuna-chinese-7b使用ShareGPT、ShareGPT-ZH、COT&COT-ZH、Leetcode、dummy等包含中英文的数据Finetune后的模型，训练代码参考FastChat。
3. fireballon/baichuan-vicuna-7b使用ShareGPT、COT和Leetcode等数据混合Finetune后的模型，训练代码参考FastChat。
4. Efficient-Tuning-LLMs支持Baichuan-7B使用Qlora进行Finetune和4bit inference。
5. fastllm是纯c++实现，无第三方依赖的大模型库，支持Baichuan-7B在手机端运行。
6. TheBloke/baichuan-7B-GPTQ对Baichuan-7B的GPTQ 4bit量化。
Baichuan-13B
介绍
Baichun-13B是继Baichuan-7B之后开发的130亿参数的开源可商用的大规模语言模型，在权威的中文和英文benchmark上均取得了同尺寸最好的效果，有如下几个特点：
- 更大尺寸、更多数据：参数量扩大到130亿，并且在高质量的预料上训练了1.4万亿tokens，超过LLaMA-13B40%，是当前开源13B尺寸下训练数据量最多的模型。支持中英文双语，使用ALiBi位置编码，上下文窗口长度为4096；
- 同时开源预训练模型和对齐模型，预训练模型是适合开发者的「基座」，而广大普通用户对有对话功能的对齐模型具有更强的需求。
- 更高效的推理：为了支持更光大用户的使用，开源了int8和int4的量化版本，相对非量化版本在几乎没有效果损失的情况下大大降低了部署的机器资源门槛，可以部署在Nvidia 3090这样的消费机显卡上。
- 开源免费可商用：Baichuan-13B不仅对学术研究完全开放，开发者也仅需要邮件申请并获得官方许可证后，既可以免费商用。
Benchmark结果
在各个权威大语言模型的中英文benchmark上进行了5-shot评测，结果如下：
C-Eval
MMLU
CMMLU
模型细节
暂时无法在飞书文档外展示此内容
推理和部署
推理所需的权重模型、源码、配置已经发布在Huging Face：Baichuan-13B-Base和Baichuan-13B-Chat。下面以Baichuan-13B-Chat为例示范多种推理方式。程序会自动从Hugging Face下载所需资源。推理前请安装依赖：
暂时无法在飞书文档外展示此内容
Python代码方式
在下述代码中，模型加载制定"device_map=auto"，会使用所有可用显卡。如需指定使用的设备，可以使用类似 "export CUDA_VISIBLE_DEVICES=0, 1"，使用了0、1号显卡的方式控制。
暂时无法在飞书文档外展示此内容
命令行工具方式
暂时无法在飞书文档外展示此内容
推理性能
测试环境和参数：GPU A100-SXM4-80G，PyTorch 2.0.0+cu117，transformer 4.29.1，batch_size=1, 生成长度=2048，精度fp16，基于Baichuan-13B-Base。
Baichuan-13B使用了ALiBi的线性偏置技术，相对于Rotary Embedding计算量更小，对推理性能有显著提升；与标准的LLaMA-13B相比，平均推理速度(tokens/s)实测提升31.6%。
暂时无法在飞书文档外展示此内容
量化部署
Baichuan-13B支持int8和int4量化，用户只需要再推理代码中简单修改代码即可。开发者可以按照自己的需求修改模型的加载方式，请注意：如果是为了节省显存而量化，应加载原始精度模型到CPU后再开始量化；避免在from_pretrained时添加device_map='auto'或者其它导致把原始精度模型直接加载到GPU的行为的参数。
如果使用int8量化：
暂时无法在飞书文档外展示此内容
如果使用int4量化：
暂时无法在飞书文档外展示此内容
另外，如果不想调用quantize在线量化，有已经量化好的int8 Chat模型可供使用：
暂时无法在飞书文档外展示此内容
量化前后占用显存情况如下：
暂时无法在飞书文档外展示此内容
量化后在各个benchmark上的结果和原始版本对比如下：
暂时无法在飞书文档外展示此内容
CPU部署
Baichuan-13B支持CPU推理，但需要强调的是，CPU的推理速度相对较慢。需按照如下方式修改模型加载方式：
暂时无法在飞书文档外展示此内容
对模型进行微调
开发者可以对Baichuan-13B-Base或Baichuan-13B-Chat进行微调使用。在此测试了与Baichuan-13B兼容的微调工具LLaMA Efficient Tuning，并给出了全量微调和LoRA微调的两种示范。在开始之前，开发者需要下载LLaMA Efficient Tuning项目并按照其要求安装依赖。
输入数据为放置在项目data目录下的json文件，用--dataset选项指定（参考下面示例），多个输入文件用','分隔。json文件示例格式和字段说明如下：
暂时无法在飞书文档外展示此内容
json文件中存储了一个列表，列表的每个元素是一个sample。其中instruction代表用户输入，input是可选项，如果开发者同时制定了instruction和input，会把二者用'\n'链接起来代表用户输入；output代表期望的模型输出。
全量微调
我们在8*Nvidia A100 80GB + deepspeed的环境下进行了全量微调。启动训练脚本示例：
暂时无法在飞书文档外展示此内容
deep_speed.json配置示例：
暂时无法在飞书文档外展示此内容
LoRA微调
在单张Nvidia A100 80G显卡上进行了LoRA微调测试。训练启动脚本示例：
暂时无法在飞书文档外展示此内容