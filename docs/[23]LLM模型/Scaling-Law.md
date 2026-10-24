解析大模型中的Scaling Law
介绍一些Scaling Laws
在大模型开发中，通常会有一些需求：
1. 计划训练一个10B的模型，想知道至少需要多大的数据？
2. 收集到了1TB的数据，想知道能训练一个多大的模型？
3. 老板准备1个月后开发布会，给的资源是100张A100，应该用多少数据训练多大的模型效果好？
4. 老板对现在10B的模型不满意，想知道扩大到100B模型的效果能提升多少？
以上这些问题都可以基于Scaling Law的理论进行回答，本文是阅读了一系列Scaling Law的文章后的整理和思考，包括Scaling Law的概念和推导以及反Scaling Law的场景。
核心结论
大模型的Scaling Law是OpenAI在2022年提出的概念，具体如下：
1. 对于Decoder-only的模型，计算量C(Flops)、模型参数量N、数据大小D(token数量)，三者满足：$$C\approx 6ND$$。
2. 模型的最终性能主要与计算量C、模型参数量N和数据大小D三者有关，而与模型的具体结构(层数/深度/宽度)基本无关。
[图片]
3. 对于计算量C，模型参数量N和数据大小D，当不受其他两个因素制约时，模型性能与每个因素都呈现出幂律关系。
[图片]
4. 为了提升性能，模型参数量N和数据大小D需要同步放大，但模型和数据分别放大的比例还存在争议。
5. Scaling Law不仅适用于语言模型，还适用于其他模型以及跨模态的任务。
[图片]
核心公式
$$L(x)=L_{\infin} + (\frac{x_0}{x})^{\alpha}$$
$$L_{\infin} \approx S(True) “Irreducible Loss"$$
$$(\frac{x_0}{x})^{\alpha} \approx D_{KL}(True||Model) “Reducible Loss”$$
- 第一项$$L_{\infin}$$是指无法通过模型规模来减少的损失，可以认为是数据自身的熵(例如数据中的噪声)；
- 第二项$$(x_0/x)^{\alpha}$$是指能通过增加计算量来减少的损失，可以认为是模型拟合分布与实际分布之间的差。
根据公式，增大x(例如计算量C)，模型整体loss下降，模型性能提升；伴随着x趋向无穷大，模型能拟合数据的真实分布，让第二项逼近0，整体趋向$$L_{\infin}$$。
大模型中的Scaling Law
GPT-4
下图是GPT4报告中的Scaling Law曲线，计算量C与模型性能能满足幂律关系；
- 横轴是归一化之后的计算量，假设GPT4的计算量是为1，基于10000倍小的计算规模，就能预测最终GPT4的性能
- 纵轴是"Bits for words"，这也是交叉熵的一个单位。在计算交叉熵时，如果使用以2为底的对数，交叉熵的单位就是"bits for word"，与信息论中的比特(bit)概念相符。所以这个值越小，说明模型性能越好。
Baichuan2
下图是Baichuan2技术报告中的Scaling Law曲线。基于10M到3B的模型在1T数据上训练的性能，可预测出最后7B模型和13B模型在2.6T数据上的性能。
[图片]
MindLLM
下图是MidLLM技术报告中的Scaling Law曲线。基于10M到500M的模型在10B数据上训练的性能，预测出最后3B模型在500B数据上的性能。
[图片]
Scaling Law 实操: 计算效率最优
根据幂律定律，模型的参数固定，无线堆数据并不能无限提升模型的性能，模型性能最终会慢慢趋向一个固定值
[图片]
如图所示，如果模型的参数量为$$10^3$$（图中的紫线），在数量上达到$$10^9$$，模型基本收敛。所以在数据量达到$$10^9$$后，继续增加数据产生的计算量，没有同样计算量下提升模型参数量带来的收益大（计算效率更优）。根据$$C=6ND$$，可以进一步转换成模型参数与计算量的关系，即：模型参数为$$10^3$$，在计算量为$$6 \times 10^{12}$$Flops，即$$7\times10^{-8}$$PF-days时基本收敛，也就是图中紫色线的拐点。
根据Baichuan的实验，在中英文场景下，7B模型收敛时的算力是$$10^{23}$$FLOPS，对应的数据量应该是$$D=\frac{10^{23}}{6*7*10^9} = 2.3T$$。
按照上面的思路，下面进行Scaling Law的实操。
首先准备充足的数据（例如1T），设计不同模型参数量的小模型（例如0.001B- 1B)，独立训练每个模型，每个模型都训练到基本收敛（假设数据量充足）。根据训练中不同模型的参数和数据量的组合，收集计算量与模型性能的关系。然后可以进一步获得计算效率最优时，即同样计算量下性能最好的模型规模和数据大小的组合，模型大小与计算量的关系，以及数据大小与计算量的关系。
[图片]
 如图所示，根据左图可以看到计算量与模型性能呈现幂律关系（可以认为数据和模型都不受限制），根据中图和右图，可以发现$$N_{opt} \varpropto C^{\alpha}$$, $$D_{opt} \varpropto C^{b}$$，即计算效率最优时，模型的参数与计算量的幂次呈现线性关系，数据量的大小也与计算量的幂次呈现线性关系。
根据$$C=6ND$$，可以推算出$$a+b=1$$，但是a、b分别是多少存在分歧。
OpenAI认为模型规模更重要，即a=0.73, b=0.27，而DeepMind在Chinchilla和Google在PaLM中都验证了a=b=0.5，即数据和模型同等重要。
所以假定计算量整体放大10倍，OpenAI认为模型参数更重要，模型参数应该放大$$10^{0.73}$$(5.32)倍，数据应该放大$$10^{0.27}$$(1.86)倍；后来DeepMind和Google认为模型和数据同等重要，二者都应该放大$$10^{0.5}$$(3.16)倍。
[图片]
例如在PaLM的实验中，计算量从$$1\times 10^{21}$$放大10倍到$$1\times 10^{22}$$，模型参数也提升了3.2倍，从3.35B到10.7B。
LLaMA：反Scaling Law的大模型
假设遵循计算效率最优来研发LLM，那么根据Scaling Law，给定模型大小，可以推算出最优的计算量，进一步根据最优计算量推算出需要的token数量，然后训练就行。但是计算效率最优这个观点是针对训练阶段而言的，并不是推理阶段，实际应用中推理效率更实用。
Meta在LLaMA中观点：给定模型的目标性能，并不需要用最优的计算效率在最快的时间内训练好模型，而应该在更大规模数据上，训练一个相对更小的模型，这样的模型在推理阶段的成本更低，尽管训练阶段的效率不是最优的（同样的算力其实能够获得更优的模型，但是模型尺寸也会更大）。根据Scaling Law，10B模型只需要200B数据，但是作者发现7B的模型性能，在1T的数据后还能继续提升。
[图片]
所以LLaMA工作的重点是训练一系列语言模型，通过使用更多的数据，让模型在有限推理资源下有最佳的性能。
具体而言，确定模型尺寸后，Scaling Law给到的只是最优的数据量，或是说是至少的一个数据量，实际在训练过程中观察在各个指标上的性能表现，只要还在继续增长，就可以持续增加训练数据。
[图片]
计算量、模型参数和数据大小的关系推导
对于Decoder-only的模型，计算量C(Flops)，模型参数量N(除去embedding的部分)，数据大小D(token数量)，三者个关系为：$$C \approx 6ND$$
推导如下，记模型结构为：
- decoder层数：$$l$$
- attention隐藏层维度：$$d$$
- Attention feedforward层维度：$$d_{ff}$$，一般来说$$d_{ff}=4*d$$
首先推导模型的参数量N（忽略embedding，norm和bias）计算如下：
- tansformer每层包括：self-attention和MLP两个部分，
  - self-attention的参数为$$W_Q,W_K,W_V,W_O$$，每个矩阵的维度均为$$R^{d\times d}$$，整体参数量为：$$4d^2$$
  - MLP的层数的参数为$$W_1 \in R^{d\times d_{ff}}$$，$$W_2 \in R^{d_{ff}\times d}$$，整体参数量：$$2*d*d_{ff}=2*d*4d=8d^2$$，
  - 因此每层的参数量为：$$4d^2+8d^2=12d^2$$，全部的$$l$$层的参数量为$$12ld^2$$，即$$N=12ld^2$$
继续推导模型的前向推理的计算量：
计算量的单位是FLOPs，floating point operations对于矩阵$$A\in R^{m\times n}, B\in R^{n\times p}$$，AB相乘的计算量是$$2mnp$$，一次加法，一次乘法。
- 假设Decoder层的输入为$$X\in R^{b\times s\times d}$$，其中b为batch size，s表示序列长度，d表示模型维度
  - self-attention的计算:
    - 输入线性层：$$XW_Q, XW_K, XW_V$$，计算量为：$$3*b*s*d*d*2=6bsd^2$$
    - attention计算：$$QK^T$$，计算量为：$$b*s*s*d*2=2bs^2d$$
    - score与V的计算：$$S_{attention}V，计算量为:b*s*s*d*2=2bs^2d$$
    - 输出线性层：$$XW_O$$，计算量为：$$b*s*d*d*2=2bsd^2$$
  - MLP部分的计算
    - 升维：$$XW_1$$，计算量为：$$b*s*2*d*4d=8bsd^2$$
    - 降维：$$XW_2$$，计算量为：$$b*s*2*4d*d=8bsd^2$$
  - decoder层的计算量为：$$24bsd^2+4bs^2d$$，全部$$l$$层为：$$C_{forward}=24lbsd^2+4lbs^2d$$
最后反向传播计算量是正向的2倍，所以全部的计算量为：$$C=3*C_{forward}=72lbsd^2+12lbs^2d$$
平均每个token的计算量为$$C_{token}=\frac{C}{bs}=72ld^2+12lsd=6N(1+\frac{s}{6d}) \approx 6N(s\ll 6d)$$
所以对于全部包含D个token的数据集：$$C=C_{token}D \approx 6ND$$
参考资料
1. Scaling Laws for Neural Language Models
2. Training Compute-Optimal Large Language Models
3. PaLM 2 Technical Report
4. Scaling Laws for Autoregressive Generative Modeling
5. GPT-4 Technical Report
6. Baichuan 2: Open Large-scale Language Models
7. MindLLM: Pre-training Lightweight Large Language Model from Scratch, Evaluations and Domain Applications
8. LLaMA: Open and Efficient Foundation Language Models
9. 人工智能中的算力单位Petaflop/s-day - 套牌神仙的文章 - 知乎
10. 李开复带队零一万物发布开源大模型 Yi，如何解读？ - 黄文灏的回答 - 知乎
11. 介绍一些Scaling Laws - cingti的文章 - 知乎
12. 分析transformer模型的参数量、计算量、中间激活、KV cache - 回旋托马斯x的文章 - 知乎