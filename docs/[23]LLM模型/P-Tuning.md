深度解读一种新的微调范式
Prompt-Tuning——深度解读一种新的微调范式_prompt tuning-CSDN博客
本文将系统介绍以下知识点：
1. 什么是预训练语言模型？
2. 什么是prompt？为什么要引入prompt？相比于fine-tuning有什么优势？
3. 自20年代开始，prompt的发展历程，那些经典的代表方法?
4. 面向不同的NLP任务，prompt如何选择和设计？
5. 面向超大规模模型，如何借助prompt进行参数有效性训练？
6. 面向GPT-3，什么是In-Context Learning? 什么是Chain-Of-Thought?
7. 面向黑盒模型，如何使用prompt？
8. ChatGPT里面有哪些prompt技术？
9. 未来prompt的发展和研究前景？
Prompt的由浅入深的理解：
1. 一级：prompt是一种对任务的指令；
2. 二级：prompt是一种对预训练目标的复用；
3. 三级：prompt本质是对参数有效性训练；
发展历程
预训练语言模型的发展历程
截止到23年3月底，语言模型发展走过了三个阶段：
1. 第一阶段：设计一系列的自监督训练目标（MLM、NSP等），设计新颖的模型架构（transformer），遵循pre-training和fine-tuning范式，典型代表是BERT、GPT、XLNet等；
2. 第二阶段：逐步扩大模型参数和训练语料规模，探索不同类型的架构，典型代表是BART、T5、GPT-3等；
3. 第三阶段：走向AIGC（Artificial Intelligent Generated Content）时代，模型参数规模步入千万亿，模型架构为自回归架构，大模型走向对话式、生成式、多模态时代，更加注重与人类进行对齐、实现可靠、安全、无毒的模型。典型代表是InstructionGPT、ChatGPT、Bard、GPT-4等；
Prompt-Tuning技术发展历程
[图片]
Prompt-Tuning自从GPT-3被提出以来，从传统的离散、连续的prompt的构建，走向面向大规模的In-context Learning、Instruction-Learning、Chain-of-Thought。
自从GPT、ELMo、BERT的相继提出，以Pre-training+Fine-tuning的模式在诸多NLP任务中被使用。其现在pre-training阶段通过一个模型在大规模无监督语料中预先训练一个预训练模型(pre-trained language model, PLM)，然后在Fine-tuning阶段基于训练好的语言模型在具体的下游任务上再次进行微调(fine-tuning)，以获得适应下游任务的模型。这种模式在诸多任务中的表现，超越了传统的有监督学习方法，不论是在工业生产、科研创新还是竞赛中均作为主流方式。然而这种模式也存在着一些问题，例如，在大多数的下游任务微调时，下游任务目标和预训练目标差距过大会导致提升效果不明显，训练过程中以来大量的监督语料。
至此，以GPT-3、PET为首提出的一种基于预训练语言模型的新的微调范式——Prompt-Tuning，其旨在通过添加模版的方法来避免引入额外的参数，从而让语言模型在小样本(few-shot)或者零样本(zero-shot)场景下达到理想效果。Prompt-Tuning又可以称为Prompt、Prompting、Prompt-based Fine-Tuning等。
因此，简单的来说，Prompt-Tuning的动机旨在解决传统Fine-Tuning的两个痛点问题：
- 降低语义差异(Bridge the gap between pre-training and fine-tuning)：预训练任务以Masked Language Model (MLM)为主，而下游任务则重新引入新的训练参数，因此两个目标通常由较大差异。因此需要解决如何缩小pre-training 和 fine-tuning两个阶段目标差异过大的问题；
- 避免过拟合(Overfiting of the head)：由于fine-tuning阶段需要引入额外的参数以适配相应的任务需要，因此在样本数量有限的情况下容易发生过拟合，降低了模型的泛化能力。因此需要面对预训练模型的过拟合问题。
预训练模型
涉及知识点：
单向语言模型、双向语言模型
Transformer
预训练任务，包括MLM、NSP等
NLP的任务类型以及fine-tuning
预训练模型主要分为两种类型：
- 单向：以GPT为首，强调从左到右的编码顺序，使用于Encoder-Decoder模式的自回归(auto-regression)模式；
- 双向：以ELMO为首，强调从左到右和从右到左的双向编码，但ELMO得主体是LSTM，由于其是串行编码导致运行速度较慢，因此BERT则以Transformer为主体结构作为双向语言的基础。
现如今常用的语言模型大多数是BERT及其变体，它的主体结构Transformer模型是谷歌机器翻译团队在2017年提出的，是一种完全利用attention基础构建的端到端模型。之所以选择Transformer，是因为其完全以attention作为计算推理技术，任意的两个token均可两两交互，使得推理完全可以有矩阵乘积来替代，实现了并行化计算，因此Transformer也可以认为是一个全连接图，缓解了序列数据普遍存在的长距离依赖和梯度消失等缺陷。
在NLP领域中，Attention机制的目标是对具有强相关的token之间提高模型的关注度。例如在文本分类中，部分词对分类产生 的贡献更大，则会分配较大的权重。
对句子的编码主要目标是为了让模型记忆token的语义。传统的LSTM则只能通过长短期记忆的方式来捕捉token之间的关系，容易导致梯度消失或记忆模糊的问题，而Transforer中任意的token之间都有显式的连接，避免了长距离依赖问题。当然，Transformer也增加了position embedding来区分不同token的位置关系。
经典的Pre-trained任务
本文的目标是介绍Prompt-Tuning的方法，而Promt-Tuning的动机是进一步拉进微调和预训练阶段的任务目标，因此本部分以BERT为主，简单介绍Pre-training的经典方法。
MLM: Masked Language Model
传统的语言模型是以Word2Vec、GloVe为代表的词向量模型，他们主要以词袋(N-Gram)为基础。例如在word2vec的CBOW方法中，随机选择了一个固定长度的词袋区间，然后挖掉中间部分的词后，让模型预测该位置的词。
MLM则采用了N-Gram的方法，不同的是，N-Gram喂入的是被截断的短文本，而MLM是完整的文本，因此MLM能够保留原始的语义。
[图片]
[图片]
MLM是一种自监督的训练方法，其先从大规模的无监督语料上通过固定的替换策略获得自监督语料，设计预训练的目标来训练模型，具体的可以描述为：
- 替换策略：在所有语料中，随机抽取15%的文本token进行mask。在被选中的文本token中，有80%的概率被替换为[mask]，10%的概率保持不变，10%的概率随机替换成其他token，其中[mask]表示没有出现过。
- 训练目标：当模型遇到[mask] token时，则根据学习到的上下文语义去预测该位置的词。因此，训练目标是对整个此表上的分类任务，可以使用交叉熵作为目标函数。
因此以BERT为例，首先喂入一个文本 It is very cold today, we need to wear more clothes. 然后随机mask掉一个token，并结合一些特殊标记得到：[cls] It is very cold today, we need to [mask] more clothes. [seq] 喂到多层的transfromer结构中，则可以得到最后一层每个token的隐状态向量。MLM则通过在[mask]头部添加一个MLP映射到词表上，得到所有词的概率分布。现如今有诸多针对MLM的改进版本，我们选两个经典的来介绍：
- Whole Word Masking（WWM）：起源于RoBERTa等，其认为BERT经过分词后得到的是word piece，而BERT的MLM则是基于word piece进行随机替换操作的，及single-token masking，因此被mask的token语义并不完整。而WWM则表示被mask的必须是一个完整的单词。
- Entity Mention Replacement（EMR）：起源于ERNIE-BAIDU等，其通常是知识增强的预训练场景，即给定已知的知识库(实体)，对文本中的整个实体进行mask，而不是单一的token或者单词。
NSP: Next Sentence Prediction
在BERT原文中，还添加了NSP任务，其主要目标是给定两个句子，判断二者之间的关系，属于一种自然语言推理(NLI)任务。在NSP中存在三种关系，分别是：
- entailment(isNext)：存在蕴含关系，NSP则任务相邻的两个句子属于entailment，即isNext关系；
- contradiction(isNotNext)：矛盾关系，NSP则认为两个句子不存在前后关系，例如两个句子来自不同的文章；
- neutral：中性关系，NSP中认为当前的两个句子可能来自同一篇文章，但是不属于isNext关系；
而显然，构建NSP语料也可以通过自监督的方式获得，首先给定一个大规模无监督语料，按照文章分类。在同一篇文章中，最近挑选一个句子作为premise，因此entailment对应的是下一个句子，另外再随机挑选同一篇文章的其它句子作为neutral类，其它文章中的句子作为contradiction类。
在BERT中，NSP任务则视为sentence-pair任务，例如输入两个句子 S1: It is very cold today. 和 S2: We need to wear more clothes.  通过拼接字符后，得到: [cls] It is very cold today. [sep] we need wear more clothes. [sep]，然后喂入到多层transfromer中，可以得到[cls]token的隐向量，同样通过MLP映射到一个三分类上获得各个类的概率。
[图片]
在ALBERT、RoBERTa等系列的模型中，由于发现NSP对实验效果没有太多正向效果，因此均删除了NSP任务，在后续的预训练模型中，也纷纷提出了其他的预训练模型。在后续的prompt-tuning技术中，大多数以MLM作为切入点。
Task-specific Fine-tuning
获得了预训练的语言模型后，在面对具体的下游任务时，则需要进行微调。通常微调的任务目标取决于下游任务的性质，简单列举几种NLP有关的下游任务。
单句分类: Single-text Classification
短/长文本分类：直接对句子进行分类，例如新闻归类、主题分类、场景识别等；
意图识别：根据给定的问句判断其意图，常用于检索式问答、多轮对话、只是图谱问答等；
情感分析：对评论类型的文本进行情感取向分类或者打分；
关系抽取：给定两个实体以及对应的一个描述类型句子，判断这两个实体的关系类型。
常见的单句分类任务有短文本分类、长文本分类、意图识别、情感分析、关系抽取等。给定一个长文本，喂入多层transformer模型中，获得最后一层的隐状态向量后，在输入到新添加的分类器MLP中进行分类。在Fine-tuning阶段中，则通过交叉信息熵损失函数训练分类器。
句子匹配: Sentence-pair Classification
语义推理/蕴含：判断两个句子是否存在推理关系，例如entialment、contradiction、neutral三种推理关系；
文本匹配/检索：输入一个文本，并从数据库中检索与之高度匹配的其它句子；
常见的匹配类型任务有语义推理、语义蕴含、文本匹配与检索等。给定两个文本，用于判断是否存在匹配关系。此时，将两个文本拼接后喂入模型中，训练策略与single-text classification一样；
区间预测: Span Text Sentence
常见的任务类型有抽取式阅读理解、实体抽取、抽取式摘要等。给定一个passage和query，根据query寻找passage中可靠的字序列作为预测答案。通常该类任务需要模型预测区间的起始位置，因此在Transformer头部添加两个分类器以预测两个位置。
字符分类: Single-token Classification
序列标注：对给定文本的每个token进行标注，通常有词性标注、槽位填充、句法分析、实体识别等；
完型填空：与MLM一致，预测给定文本中空位处可能得词；
拼写检测：对给定的文本寻找在语义/语法中的拼写错误，并进行纠正；
此类涵盖序列标注、完型填空、拼写检测等任务，获得给定文本的隐状态后喂入MLP中，得到每个token对应的预测结果，并采用交叉熵进行训练。
文本生成: Text Generation
生成式摘要：在文本摘要中个，通过生成方法获得摘要；
机器翻译：给定原始语言的文本，生成目标语言的翻译句子；
问答：给定query，直接生成答案；
文本生成任务常用于生成式摘要、机器翻译、问答等。通常选择单向的预训练模型实现文本的自回归生成，也有部分研究在探索非自回归的双向transformer进行文本生成任务。BART结合单向和双向实现生成任务。
[图片]
这几类任务几乎可以涵盖所有自然语言处理场景中，而这五类任务在fine-tuning阶段几乎都涉及在模型头部引入新参数的情况，且都存在小样本场景过拟合的问题，因此prompt-tuning的引入非常关键。
Prompt-Tuning的研究进展
Prompt-Tuning的定义
template和verbalizer的定义；
那什么是prompt呢？在了解预训练模型的基础，以及预训练语言模型的在pre-training和fine-tuning之后，我们已经可以预想到prompt的作用是将fine-tuning的下游任务目标转化为pre-training目标。那么具体如何工作呢？
以情感二分类为例，描述prompt的工作原理。给定一个句子，[CLS] I like the Disney films very much. [ESP]. 传统的Fine-tuning方法是通过BERT的Transformer获得 [CLS]表征之后，再喂给新增加的MLP分类器进行二分类，预测该句子是积极的(positive)还是消极的(negative)，因此需要一定量的训练数据来训练。
而Prompt-Tuning则执行如下步骤：
- 构建模板(Template Construction)：通过人工定义、自动搜索、文本生成方法等，生成与给定句子相关的一个含有[mask]标记的模板。例如It was [mask]. 并拼接到原始的文本中，获得Prompt-Tuning的输入: [CLS] I like the Disney films very much. [SEP] It was [MASK]. [SEP]。将其喂入到BERT模型中，并复用预训练好的MLM分类器（在huggingface中为BERTForMaskedLM），既可以直接得到[MASK]预测的各个token的概率分布。
- 标签词映射(Label)：因为[MSAK]部分我们只对部分词感兴趣，因此需要建设一个映射关系。例如如果[MASK]预测的词是“great”，则认为是positive类，如果是“terrible”，则认为是negative类。
此时会有人想到，不同的句子应该有不同的template和label word，地区如此，因为每个句子可能期望预测出来的label word都不相同，因此如何最大化的寻找更加合适的template和label word是prompt-tuning非常重要的挑战。
- 训练：根据Verbalizer，则可以指定label word的预测概率分布，并采用交叉熵进行训练，因为此时只对训练好的MLM的head进行微调，所以避免了过拟合问题。
- 在hugging face中可以直接测试：
  - I like the film very much.
  - I dislike the films very much.
[图片]
[图片]
GPT-3
Prompt的形式化定义、Prompt的集成
经典的template的构建方法——启发式、生成式、连续提示、混合提示
经典的verbalizer的构建方法——启发式、连续式
那么prompt-tuning具体如何实现，其有什么挑战和困难呢？将会详细介绍prompt-tuning在学术上的发展历程。
Prompt-Tuning的鼻祖—GPT-3与PET
Prompt-Tuning起源于GPT-3的提出《Language Model is Few-Shot Learners》(NIPS2020)，其认为超大规模的模型配合合适的模版就可以极大化地发挥出其理解和推理能力。其开创性地提出in-context learning概念，即无须修改模型就可以实现few-shot/zero-shot learning。同时引入demonstrate learning，即让模型知道与标签相似的语义描述，提升推理能力。
- In-context Learning：是prompt的前身，其通过从训练集中挑选一些样本作为任务的提示（Natural Language Prompt），来实现避免参数更新的模型预测；
- Demonstration Learning：添加一些新的文本作为提示。例如在对“I like the film. It was [MASK]”进行情感分析时，可以根据一些相似场景的ground-truth文本“I like the book, it was great.”、“The music is boring. It is terrible for me.”等。此时模型在根据新加的两个样例句子就可以“照葫芦画瓢”式地预测结果了。
不过以GPT-3为首的这类方法有一个明显的缺陷是——其建立在超大规模的预训练语言模型上，此时的模型参数量通常超过100亿，在真实场景中很难应用。因此众多研究开始探索GPT-3在小规模的语言模型（BERT）上是否使用？事实上，这套方法在小规模的语言模型上是可行的，但是需要注意几点：
- 模型参数规模变小了，Prompt直接用在Zero-shot上效果会下降，因此需要考虑将in-context learning和demonstrate learning应用在fine-tuning阶段；
- GPT-3提供的提示(Natural Language Prompt)过于简单，并不难使用在一些具体的任务场景，因此需要单独设计一套组件实现；
因此，大名鼎鼎的PET模型问世，PET(Pattern-Exploiting Training)出自Exploiting Cloze-Questions for Few-Shot Text Classification and Natural Language Inference，根据论文题目可以猜出，Prompt-Tuning启发与文本分类任务，并且试图将所有的分类任务转换为与MLM一致的完型填空。PET详细地设计了Prompt-Tuning的重要组件--Pattern-Verbalizer-Pair(PVP)，并描述了Prompt-tuning如何实现Few-shot/Zero-shot Learning，如何应用在券监督和半监督场景(iPET)。PET设计了两个很重要的组件：
- Pattern（Template）：记作T，即上文提到的template，其为额外添加的带有[mask]标记的短文本，通常一个样本只有一个Pattern。上文也提到，不同的任务、不同的样本可能会有更加合适的pattern，因此如何构建合适的pattern是Prompt-Tuning的研究重点之一。
- Verbalizer：记作V，即标签词的映射，对于具体的分类任务，需要选择制定的标签词（label word）。例如情感分析中，我们期望Verbalizer可能是V(positive)=great，V(negative)=terrible（positive和negative是类标签）。同样，不同的任务有其相应的label word，但需要注意的是，Verbalizer的构建需要取决于对应的Pattern。因此如何构建Verbalizer是另一个重要研究。
- 上述两个组件被称为Pattern-Verbalizer-Pair(PVP)，一般记作P=(T, V)，在后续的大多数研究中均采用这种PVP组件。
因此基于PVP的训练目标可以形式化描述：
给定一个句子x，以及对应的标签y，给定定义的PVP组件P=(T, V)，则有：
$$p(y|x)=\prod_{j=1}^{n}p([mask]_j=V(y)|T(x))$$
一般情况下，一个句子只能有一个PVP（因为我们只需要一个[mask]用来预测），这可能并不是最优的，是否可以为一个句子设计多个不同的PVP呢？这是可以的，属于prompt-tuning的集成。PET提供了简单的集成思路：
- Patterns Ensembling：同一个句子设计多个不同的pattern，例如It was [mask]. I think it is [mask]. This comment denotes as [mask]. 等。此时，原先只需要一个句子，确可以生成多个不同的样本，也变相起到数据增强的作用。在训练时，可以当做单独的样本进行训练；推理时，则可以对所有pattern的结果进行加权投票或者加权。
- Verbalizers Ensembling：同样，在给定的某个pattern下，并非只有一个词可以作为label word。例如positive类，则可以选择great、nice、wonderful。当模型预测出这三个词的时候，均可以判断为positive类。在训练和推理时，可以对所有label word的预测概率进行加签或者投票处理，并最后获得概率最大的类。
[图片]
- PVPs Ensembling（Prompt Ensembling）：Patter和Verbalizer均可进行集成，此时同一个句子有多个pattern，每个pattern又对应多个label word。在训练时可以采用加权，在推理时可以采用加权或者投票法。
[图片]
- PET还提供了半监督的学习方法——iterative PET（iPET），如下图所示：
iPET旨在先从预训练模型开始，初始化多个不同的模型（如图1步骤），在有标注的少量样本上进行prompt-tuning，然后通过多个不同的PVP训练得到多个不同的模型（图中a步骤），每个模型在无标注数据上进行推理打标，并根据置信度筛选（图中b所示），根据新标注的数据和原始标注数据融合后，再重新进行prompt-tuning（图中c所示），重复abc三个步骤多次后，获得每个模型后，在测试进行集成投票（图中2、3步骤）。
因此可以说，PET提供prompt-tuning比较成熟的框架-PVP，基于这套框架，目前的研究开始关注如何选择或构建合适的pattern和verbalizer。一种简单的方式是根据特定任务的性质和先验知识人工设计模版。例如上文例子中通常会选择It was [mask]. 作为情感分析类的模板。人工构建方式虽然直观简单，但是致命问题也很突出。有相关工作在实验中发现，在同样的数据集和训练条件下，选择不同的Pattern和Verbalizer会产生差异很大的结果，如下图所示（一般情况下，Template等同于Pattern，Verbalizer等同于Label Word）：
可发现，在相同Pattern时，选择不同的label word对结果影响很大，同理，不同的pattern对结果影响也显而易见。在真正应用中，调参者需要尝试不同的目标和标签词以穷举最好的结果，并补充充分发挥prompt简单快捷的优势。因此我们总结出人工设计方法的缺陷：
- 采用人工构建的方法成本高，需要与领域任务相关的先验知识；
- 人工设计的Pattern和Verbalizer不能保证获得最优解，训练不稳定，不同的PVP对结果产生的差异明细，方差大；
- 在预训练阶段MLM任务并非完全按照PVP的模式进行训练的（比如MLM训练通常都是长文本，mask的数量也并非只有1个，预测的概率分布也并非是有限的），因此人工构建的Pattern和Verbalizer使得Prompt-Tuning与MLM在语义和分布上依然存在差异。
如何挑选合适的Pattern？
自2020年底至今，学术界已经涌现出一批基于Prompt-Tuning的方案试图探索如何构建PVP。本节主要总结几种成熟的Pattern（Template）构建方法。可以罗列以下几点：
- 人工构建（Manual Template）
- 启发式法（Heuristic-based Template）：通过规则、启发式搜索等方法构建合适的模板；
- 生成（Generation）：根据给定的任务训练数据（通常是小样本场景），生成合适的模板；
- 词向量微调（word Embedding）：显式地定义离散字符的模板，但在训练时这些模板字符的词向量参与度下降，初始定义的离散字符用于作为向量的初始化；
- 伪标记（Pseudo Token）：不显式地定义离散的模板，而是将模板作为可训练的参数；
前面3种也被称为离散的模板构建方法(记作Hard Template、Hard Prompt、Discrete Template、Discrete Prompt)，其旨在直接与原始文本拼接显式离散的字符，且在训练中始终保持不变。这里的保持不变是指这些离散字符的词向量（Word Embedding）在训练过程中保持不变。通常情况下，离散法不需要引入任何参数。
后面2种则被称为连续的模板构建方法(记作Soft Template、Soft Prompt、Continuous Template、Continuous Prompt)，其旨在让模型在训练过程中根据具体的上下文语义和任务目标对模板参数进行连续可调。这套方案的动机则是认为离散不变的模板无法参与模型的训练环节，容易陷入局部最优，而如果将模版变成可训练的参数，那么不同的样本都可以在连续的向量空间中寻找合适的伪标记，同时也增加模型的泛化能力。因此，连续法需要引入少量的参数并让模型在训练时进行参数更新。
下面介绍2种经典的方法：
- 启发式构建模板
启发式法一般是采用规则、正则化模板的方法自动构建出相应的pattern，或者直接通过启发式搜索的方法获得Pattern。这一类方法在程序设计时只要编写规则和少量的模板即可快速的获取Pattern。
给定一个具体的任务(例如分类任务)，可以实现定义若干个模板(例如正则化工具)，然后根据具体的句子内容，向模板中填充相关实体，以贴合句子实际的描述。
- 生成法构建模板
基于规则的方法构建的模板虽然简单，但是这些模板都是“一个模子刻出来的”，在语义上其实挺难做到与句子贴合。因此一种策略就是直接让模型来生成合适的模板，因为文本生成本质上就是去理解原始文本的语义，并获得在语义上较为相关的文本。
- 连续提示模板
不论是启发式方法，还是通过生成式方法，都需要为每一个任务单独设计对应的模板，因为这些模板都是可读的离散的token(这类模板我们称作Discrete Prompt或者Hard Prompt)，这导致很难寻找最佳的模板。另外，即便是同一个任务，不同的句子也会有其所谓最佳的模板，而且有时候，即便是人类理解的相似的模板，也会对模型预测结果产生很大差异。
- Template优化进阶
我们为任务设计的模板都是建立在一个假设上：即模板都是尽可能是可读的，即满足人类语言的语法形态。然而最近也有工作认为，最有的模板可能是不符合语法的乱语(Ungrammatical Gibberrish Text)，即人类可读的模板，模型也许不可读。虽然这很反直觉，但是我们不能否认这种情况的存在。
Prompt-Tuning论文
基于连续提示的Prompt-Tuning的实现方法，以下三篇论文为代表，分别简要介绍：
- The Power of Scale for Parameter-Efficient Prompt Tuning，代表方法为Prompt Tuning
- GPT Understands, Too，代表方法为P-tuning
- PPT: Pre-trained Prompt Tuning for Few-shot Learning，代表方法为PPT
Prompt Tuning
该方法率先提出了伪标记和连续提示的概念，以让模型在能动态地对模板在语义空间内进行调整，使得模板是可约的（differentiate）。
每个伪标记的初始化可能有几种情况：
- 最简单的是随机初始化：随机初始化一个面向所有伪标记的embedding table，可以采用正态分布或者均匀分布；
- 每个token使用预训练模型已有的embedding table进行初始化，此时，每一个伪标记线随机指定词表中的一个词，并取对应词的embedding作为这个伪标记的初始化；
- 在分类任务上，使用label word(verbalizer)对应的embedding作为初始化，可以有效限制模型输出的是预设的输出类对应的word。
因此，在训练过程中，每个伪标记以及对应的MLP参数都可以得到训练，对于不同的输入句子x，这些伪标记对应的embedding也各不相同，达到了预期目的。
P-tuning
P-tuning是另一个具有代表性的连续提示方法。
PPT(Pre-trained Prompt Tuning)
Prompt-Tuning通常适用于地资源场景，但是由于连续的模板是随机初始化的，即其存在新的参数，少量样本可能依然很难确保这些模板被很好的优化。因此简单的方法就是对这些连续的模板进行预训练。PPT旨在通过让这些连续提示在大量无标注的预训练语料进行预训练，然后将其加载到对应下游任务的PLM上进行训练。
Prompt-Tuning的本质
设计知识点：
- 元学习与prompt
- 基于Prompt的NLP任务的统一范式
- 基于生成模型的Prompt
- Prompt与参数有效性学习
前面章节介绍了大量与Prompt相关的内容，我们可以发现，最初的Prompt Tuning是旨在设计Template和Verbalizer（即Pattern-Verbalizer Pair）来解决基于预训练模型的小样本分类，然而事实上，NLP领域涉及到很多除了分类以外其他大量复杂的任务，例如抽取、问答、生成、翻译等。这些任务都有独特的任务特性，并不是简单的PVP就可解决的，因而，我们需要提炼出Prompt Tuning的本质，将Prompt Tuning升华到一种更加通用的方式上。
博主根据对Promt-Tuning两年多的研究经验，总结了三个关于Prompt的本质，如下：
- Prompt的本质是一种对任务的指令；
- Prompt的本质是一种对预训练任务的复用；
- Prompt的本质是一种参数有效性学习；
Prompt是一种针对任务的指令
Prompt本质上对下游任务的指令，可以作为一种信息增强。简单来说，就是告诉模型需要做什么任务，输出什么内容。提及到的离散或者连续的模板，本质上就是一种对任务的提示。
看似设计指令是一件很容易的事情，但是在真实使用的过程中，预训练模型很难“理解”这些指令，根据最新研究工作发现，主要总结如下几个原因：
- 预训练模型不够大
- 缺乏指令相关的训练
TransPrompt
该方法是连续提示模板的，其对P-tuning做了如下改进：
- 引入Cross-task Learning：原来P-tuning只对单一任务进行Prompt-Tuning，而TransPrompt则对同一类别多个任务进行Cross-task Learning。
- 引入去偏（De-basing）技术：无论是小样本还是全量数据，即便是统计分布上完全一致，不同任务的难易程度是不一样的，因此模型在训练的时候可能极易偏向于一些简单任务。为了确保任务之间训练的平衡性，引入两个去偏技术，分别是Prototypical-based Debasing和Entropy-based Debiasing。
Meta Prompt Tuning（MPT）
该方法是面向离散的提示，其主要关注于文本分类任务，但不同的是，其对分类的范式进行了一些转换，将所有分类任务定义为Yes/No问题，下面对比一些两种不同范式。
复用预训练目标-实现基于Prompt的统一范式
上诉所讲的内容为什么要设计Template和Verbalizer？为什么都要包含mask token？我们发现目前绝大多数的双向预训练语言模型都包含Masked Language Modeling(MLM)，单向预训练模型都包含Autogressive Language Modeling(ALM)，这些任务都是预训练目标，本质上都是预测被mask位置的词，在训练时候让模型理解语言的上下文信息。之所以设计Template和指令，就是希望在下游任务时能够复用这些预训练的目标，避免引入新的参数而导致过拟合。因此，我们可以将Prompt升华到一个新的高度，即Prompt Tuning的本质上是复用预训练语言模型在预训练阶段所使用的目标和参数。
基于Huggingface的预训练模型仓库中，我们一般称之为LMhead，本质上就是一个MLP，输入为一个大小为[batch_size, sequence_length, hidden_size]的张量，输出为[batch_size, sequence_length, vocab_size]的概率分布。
由于绝大多数的语言模型都采用MLM或者ALM进行训练，所以我们现如今所看到的大多数基于Prompt的分类都要设计Template和Verbalizer。那么我们是否可以极大化地利用MLM和ALM的先验知识在不同的下游任务上获得更好的表现？
我们介绍两个充分利用这个思想的方法：
- 万物皆可生成：将所有任务统一为文本生成，加大化利用单向语言模型目标；
- 万物皆可抽取：将所有任务统一为抽取式阅读理解，并设计抽取式预训练目标；
- 万物皆可推理：将所有任务建模为自然语言推断（Natural Language Inference）或者相似度匹配任务；
万物皆可生成：基于生成的Prompt范式统一
在含有单向Transformer的语言模型中（例如GPT、BART），都包含自回归训练目标，即基上一个token来预测当前的token，而双向语言模型中的MLM可以视为只生成一个token的自回归模型，为此，我们则可以将分类任务视为一种特生的文本生成，并配上Verbalizer，这样，所有NLP任务都可以统一为生成任务。针对不同的任务，只需要提供对应的指令和模板即可（由于是使用单向语言模型，因此没有mask token，需要生成的部分置于文本末尾）。
ChatGPT则是基于“万物皆可生成”的思想，将单向语言模型的ALM发挥极致，实现对所有任务的大一统，与之为代表的还有In-Context Learning、Instruction-Tuning和Chain-of-Thought，
万物皆可抽取：基于抽取式阅读理解的Prompt范式统一
基于生成的方法存在两个缺点：
- 必须让待生成的部分置于文本末尾，此时会约束指令和模板的设计，不利于灵活运用；
- 由于是开放式生成，生成的内容无法控制，且依赖文本的长度等；
- 对于一些具体有条件限制的任务，例如多项选择、信息抽取等，生成的内容或许不符合这些条件。例如在做实体抽取的时候，需要确保生成的实体是在文本中出现的。
万物皆可推理：基于NI的Prompt范式统一
另外一个方式则是将所有任务建模为NLI形式，其与上文介绍的MPT比较类似，除了MPT以外，EFT(Entailment as Few-Shot Learner)和NSP-BERT也是类似的方法，其思想是复用BERT的Next Sentence Prediction(NSP)的训练目标。
Prompt的本质是参数有效性学习
根据前文的讲解，我们可以发现，实现Prompt-Tuning只需要考虑如何设计模板或者指令，而模型和训练目标则都是复用预训练阶段的，即在整个训练过程中，无需添加任何参数，而其它参数都是训练好的。基于这个思想，我们再一次将Prompt升华到更高的层面——Prompt的本质上是参数有效性学习(Parameter-Efficient Learning, PEL)。
参数有效性学习的背景：在一般的计算资源条件下，大规模的模型（例如GPT-3）很难再进行微调，因为所有的参数都需要计算梯度并进行更新，消耗时间和空间资源。为了解决这个问题，参数有效性学习被提出，其旨在确保模型效果不受太大影响的条件下尽可能提高训练的时间和空间效率。
参数有效性训练：在参数有效性学习过程中，大模型只需要指定或额外添加少量的可训练参数，而其他的参数全部冻结，这样可以大大提升模型的训练效率的同时，确保指标不会受到太大影响。
Adapter-Tuning
Adapter-Tuning在2019年提出，其面向预训练语言模型的参数有效性学习。在多层Transformer模型中，在微调过程中所有的参数都需要更新，显然并不是有效的。为了提高效率，该方法提出了固定全部Transfromer的全部参数，然后在Transformer的每一个Block里面嵌入一些新初始化的Adapter Networkd。
Adapter位于Feed-Forward Layer之后、残差连接之前。Adapter本质上就是两层MLP，分别负责将Transformer的表征降维和升维。基于Adapter的方法，只需要添加不到5%的可训练参数，即可以几乎达到全参数训练的效果，在训练过程中大大节省了训练时间，做到时间有效性。因此在真实场景应用时，不同的任务我们不需要重新对整个预训练模型进行微调，我们只需保存Adapter即可，而预训练模型的其他参数都是原始预训练的，这样就做到了空间的有效性。
Prefix-Tuning
Prefix-Tuning也是很经典的参数有效性学习，其实受到Promt-Tuning的启发。我们说Prompt-tuning的本质是参数有效性学习，是因为真个预训练模型参数可以全部固定，只需要对Template对应的少量参数（例如连续模板的Prompt Encoder、伪标记对应的Embedding等)进行训练。在Prefix-tuning中，则是除了对输入层添加模板外，还对Transformer的每一层添加模板。Prefix-Tuning与传统fine-tuning的对比图如下
可以看到，Transformer的参数完全固定，而我们只需要对prefix部分进行训练即可，对于不同的任务训练不同的prefix，在实际使用中，挑选任务相关的prefix和transformer进行组装，实现可插式的应用。
有相关工作对Adapter、Prefix-Tuning、LoRA等参数有效性学习进行了集成，因为这些参数有效性学习方法本质上都是插入少量新的参数，这些新的参数可以对预训练模型起到提示作用，只不过并不是以人类可读的离散的模板形式体现而已。
BitFit
BitFit思想更简单，其不需要对预训练模型进行任何改动，只需要指定神经网络的偏向（bias）为可训练参数即可，BitFit的参数量只有不到2%，但实验效果可以接近全量参数。
面向超大规模模型的Prompt-Tuning
Prompt-Tuning发展的两年来，有诸多工作发现，对于超过10亿参数量的模型来说，Prompt-Tuning所带来的增益远远高于标准的Fine-Tuning，小样本甚至零样本的性能也能够极大地被激发出来，得益于这些模型的参数量够大，训练过程中使用了足够多的语料，同时设计的预训练任务足够有效。最为经典的大规模语言模型则是2020年提出的GPT-3，其拥有大约1750亿的参数，且发现只需要世界诶合适的模板或者指令即可实现免参数训练的零样本学习。
本文以GPT-3为例，介绍几个面向超大规模的Prompt-Tuning方法，分别为：
- 上下文学习 In-Context Learning（ICL): 直接挑选少量训练样本作为该任务的提示；
- 指令学习 Instruction-tuning：构建指令任务集，促使模型根据任务指令做出反馈；
- 思维链 Chain-of-Thought（CoT）：给予或激发模型具有推理和解释的信息，通过线性链式的模式指导生成合理的结果。
In-Context Learning(上下文学习)
In-Context Learning（ICL）最早在GPT-3中提出，旨在从训练集中挑选少量的标注样本，设计任务相关的指令形成提示模板，用于指导测试样本生成相应的结果。
Instruction-Tuning（指令学习）
面向超大规模模型的第二个prompt技术是指令学习，在上文我们介绍过，prompt的本质之一是任务的一种指令，因此，在大规模模型微调时，可以为各种类型的任务定义指令，并进行训练，来提高模型对不同任务的泛化能力。
Chain-of-Thought（思维链）
思维链在2022年初由谷歌团队提出，其旨在进一步提高超大规模模型在一些复杂任务上的推理能力。认为现有超大规模模型存在以下问题：
- 增大模型参数规模对于一些具有挑战性任务的效果并未证明；
- 期望探索如何对大模型进行简单的推理工作；
因此，提出思维链(Chain-of-thought)，其定义如下：
A chain of thought is a series of intermediate natural language reasoning steps that lead to the final output, and we refer to this approach as chain-of-thought prompting. 
直观理解很简单，思维链是一种特殊的In-Context Learning，对于每个挑选的In-Context Example，除了给出Input-Output Mapping外，还要给出一个推理过程，称为Relationale或者Reasoning Path，其是一个具有逻辑推理功能的短文本。