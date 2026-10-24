https://openai.com/research/video-generation-models-as-world-simulators
解读
Sora是怎么训练出来的
我在模拟世界！OpenAI刚刚公布Sora技术细节：是数据驱动物理引擎
关键词：潜码(latent code)、时空块(spacetime patches)、扩展(scaling)、通用模拟器(general purpose simulators)
OpenAI用一句话概括：“我们利用了一种在视频和图片潜码上的时空块上操作的transformer架构”。具体来说就是：这群人训练了一个网络，用于降低视觉数据的维度，许多专家认为这个数据源是Youtube。这个网络以原始视频为输入，输出一个在时间和空间上都被压缩的表示。Sora在这个压缩的潜在空间中训练，随之也在此空间中生成视频。他们还训练了一个解码器模型，将生成的潜码映射会像素空间。
许多之前的研究已经通过各种方法研究了视频数据的生成模型，包括循环网络、生成对抗网络、自回归变化器和扩散模型。这些工作通常专注于视觉数据的一个狭窄类别、较短的视频或者固定大小的视频。Sora是一个视觉数据的通用模型，它可以生成跨越不同持续时间、宽高比和分辨率的视频和图像，最长可达一分钟的高清视频。
Sora是一个扩散模型，给定输入的噪声块和信息条件(例如提示文本)，它被训练用于预测初始的“干净”块。重要的是，Sora是一个扩撒transformer，在多个领域中展示了显著的扩展性能，包括语言建模、计算机视觉和图像生成。
Sora可以适应宽屏1920x1080p、竖屏1080x1920p视频以及它们之间的所有格式。这使得Sora能够直接以不同设备的原生宽高比创建内容，它还允许在使用相同模型和全分辨率生成之前，快速原型化小尺寸的内容。
简单来说，OpenAI集大成了先前的技术，在前人及同行的研究基础之上构建出Sora，一个重要的原因是：他们坚信“数据-transfromer-扩散-涌现”这一法则。
===================================================================================
有人第一时间总结道，Sora不是一个简单的视频生成器，他是一个数据驱动的物理引擎，其对于虚拟和现实世界进行模拟。在这个过程中，模拟器通过一些去噪和梯度学习方法来学习复杂的视觉渲染，构建出直观的物理效果，以及进行长期语义推理和语义基础。 
OpenAI探索了视频生成模型的大规模训练。具体来说，研究人员在可变持续时间、分辨率和宽高比的视频和图像的基础上联合训练了一个文本扩散模型。在技术报告中重点展示了：将所有视觉数据转换为统一表示，从而能够大规模训练生成模型的方法；以及对Sora的能力和局限性进行定性评估。
视觉数据转化为patches
大型语言模型在互联网规模的数据上进行训练，从获得出色的通用能力中汲取了灵感。LLM得以确立新范式，部分得益于创新了token的使用方法，研究人员巧妙地将文本的多种模态-代码、数学和语言统一了起来。
在这项工作中，OpenAI考虑了生成视觉数据的模型如何继承这种方法的好处。LLM有文本token，而Sora有视觉patches，且此前的研究已经证明patches是视觉数据模型的有效表示。OpenAI是训练生成各类视频和图像模型的可扩展且有效的标识。
在更到层面上，OpenAI首先将视频压缩到较低维度的潜在空间，然后将表示分解为时空patches，从而将视频转换为pathches。
视频压缩网络
OpenAI训练了一个降低视觉数据维度的网络，该网络将原始视频作为输入，并输出在时间和空间上压缩的潜在表示。Sora在这个压缩的潜在空间中接受训练，而后生成视频。OpenAI还训练了相应的解码器模型，将生成的潜在表示映射回像素空间。
时空潜在patches
给定一个压缩的输入视频，OpenAI提取一系列时空patches，充当Transformer的tokens。该方案也使用于图像，因为图像可视为单帧视频。OpenAI基于patches的表示使Sora能够对不同分辨率、持续时间和长宽比的视频和图像进行训练。在推理时，OpenAI可以通过在适当大小的网络中排列随机初始化的pathches来控制生成视频的大小。
用于视频生成的缩放Transformer
Sora是个扩散模型：给定输入噪声patches(以及文本提示等调节信息)，训练出的模型预测原始的“干净”的pathes。重要的是，Sora是一个扩散Transfromer。Transformer在各个领域都表现出了卓越的缩放性能，包括语言建模、计算机视觉、图像生成。
在这项工作中，OpenAI发现扩散Transformer也可以有效地缩放为视频模型，下图，OpenAI展示了训练过程中具有固定种子和输入的视频样本的比较。随着训练计算的增加，样本质量显著提高。
可变的持续时间、分辨率、宽高比
过去的图像和视频生成方法通常需要调整大小、进行裁剪或者将视频剪切到标准尺寸，例如4秒的视频分辨率为256x256。相反，该研究发现在原始大小的数据上进行训练，可以提供一下好处：
首先采样的灵活性：Sora可以采样宽屏视频1920x1080p，垂直视频1080x1920p以及两者之间的视频。这使得Sora可以直接以其天然纵横比为不同设备创建内容。Sora还允许在生成全分辨率的视频之前，以较小的尺寸快速创建内容原型，所有的内容都是用相同的模型。 
其次是改进帧和内容组成：研究者通过实证发现，使用视频的原始长度比进行训练可以提升内容组成和帧的质量。将Sora在与其它模型的对比中，后者将所有训练视频裁剪成正方形，这是训练视频生成模型的常规做法。
语言理解
训练文本到视频生成系统需要大量带有带有文本字幕的视频。研究团队将DALL.E3中的重字幕技术(pre-captioning)应用于视频。
具体来说，研究团队首先训练一个高度描述性的字幕生成性模型，然后使用它为训练集中所有视频生成字幕。研究团队发现，对高度描述性字幕进行训练可以提高文本保真度和视频的整体质量。
与DALL.E3类似，研究团队还利用GPT将简单的用户prompt转化为较长的详细字幕，然后发送到视频生成模型，这使得Sora能够生成遵循用户prompt的高质量视频。
以视频和图像作为提示
我们已经看到了文本到视频的诸多生成示例。实际上，Sora还可以使用其它输入，例如已有的图片或者视频。这使得Sora能够执行多种图像和视频编辑任务 - 创建完美的循环视频、静态图像动态化、向前或者向后延长视频。
视频内容拓展
Sora还能够在开头或者结尾拓展视频内容。
视频到视频编辑
扩散模型激发了多种根据文本prompt编辑图像和视频的方法。OpenAI将其中一种方法SDEdit应用于Sora，使得Sora能够在零样本(zero-shot)条件下改变视频的风格和环境。
连接视频
我们还可以使用Sora在两个输入视频之间逐渐转场，从而在具有完全不同的主题和场景的视频之间，创建无缝过渡。
图像生成能力
Sora还能生成图像，为此OpenAI将高斯噪声patches排列在空间网格中，时间范围为一帧。
模型涌现能力
OpenAI发现，视频模型在经过大规模训练后，会表现出许多有趣的新能力。这些能力使Sora能够模拟物理世界中人、动物和环境的某些方面。这些特性的出现，没有任何明确的三维、物体等归纳偏差 - 它们纯粹是规模现象。
三维一致性。Sora可以生成动态相机运动的视频，随着摄像机的移动和旋转，任务和场景元素在三维空间中的移动是一致的。
长序列连贯性和目标持久性。视频生成系统面临的一个重大挑战是对长视频采样保持时间一致性。OpenAI发现，Sora虽然并不总是能有效地模拟长距离和短距离的依赖关系，但它在很多时候仍然能做到这一点。
模拟数字世界。Sora还能模拟人工进程，视频游戏就是一个例子。Sora可以通过策略同时基本控制Minecraft中的玩家，同时高保真地呈现世界及其动态。
局限性讨论
作为一款模拟器，Sora还有很多局限性，例如，它不能准确模拟许多基本交互的物理现象。不过，Sora所展现的能力证明了持续扩大视频模型的规模是一个充满希望的方向，这也将助力物理和数字世界及其物体、动物和人类能有由更加精准的模拟。
原文：
Video generation models as world simulators
We explore large-scale training of generative models on video data. Specifically, we train text-conditional diffusion models jointly on videos and images of variable durations, resolutions and aspect ratios. We leverage a transformer architecture that operates on spacetime patches of video and image latent codes. Our largest model, Sora, is capable of generating a minute of high fidelity video. Our results suggest that scaling video generation models is a promising path towards building general purpose simulators of the physical world.
This technical report focuses on (1) our method for turning visual data of all types into a unified representation that enables large-scale training of generative models, and (2) qualitative evaluation of Sora’s capabilities and limitations. Model and implementation details are not included in this report.
Much prior work has studied generative modeling of video data using a variety of methods, including recurrent networks,(1,)(2,)(3) generative adversarial networks,(4,)(5,)(6,)(7) autoregressive transformers,(8,)(9) and diffusion models.(10,)(11,)(12) These works often focus on a narrow category of visual data, on shorter videos, or on videos of a fixed size. Sora is a generalist model of visual data—it can generate videos and images spanning diverse durations, aspect ratios and resolutions, up to a full minute of high definition video.
Turning visual data into patches
We take inspiration from large language models which acquire generalist capabilities by training on internet-scale data.(13,)(14) The success of the LLM paradigm is enabled in part by the use of tokensthat elegantly unify diverse modalities of text—code, math and various natural languages. In this work, we consider how generative models of visual data can inherit such benefits. Whereas LLMs have text tokens, Sora has visual patches. Patches have previously been shown to be an effective representation for models of visual data.(15,)(16,)(17,)(18) We find that patches are a highly-scalable and effective representation for training generative models on diverse types of videos and images.
At a high level, we turn videos into patches by first compressing videos into a lower-dimensional latent space,(19) and subsequently decomposing the representation into spacetime patches.
Video compression network
We train a network that reduces the dimensionality of visual data.(20) This network takes raw video as input and outputs a latent representation that is compressed both temporally and spatially. Sora is trained on and subsequently generates videos within this compressed latent space. We also train a corresponding decoder model that maps generated latents back to pixel space.
Spacetime latent patches
Given a compressed input video, we extract a sequence of spacetime patches which act as transformer tokens. This scheme works for images too since images are just videos with a single frame. Our patch-based representation enables Sora to train on videos and images of variable resolutions, durations and aspect ratios. At inference time, we can control the size of generated videos by arranging randomly-initialized patches in an appropriately-sized grid.
Scaling transformers for video generation
Sora is a diffusion model(21,)(22,)(23,)(24,)(25); given input noisy patches (and conditioning information like text prompts), it’s trained to predict the original “clean” patches. Importantly, Sora is a diffusion transformer.(26) Transformers have demonstrated remarkable scaling properties across a variety of domains, including language modeling,(13,)(14) computer vision,(15,)(16,)(17,)(18) and image generation.(27,)(28,)(29)
In this work, we find that diffusion transformers scale effectively as video models as well. Below, we show a comparison of video samples with fixed seeds and inputs as training progresses. Sample quality improves markedly as training compute increases.
[图片]
[图片]
Variable durations, resolutions, aspect ratios
Past approaches to image and video generation typically resize, crop or trim videos to a standard size—e.g., 4 second videos at 256x256 resolution. We find that instead training on data at its native size provides several benefits.
Sampling flexibility
Sora can sample widescreen 1920x1080p videos, vertical 1080x1920 videos and everything inbetween. This lets Sora create content for different devices directly at their native aspect ratios. It also lets us quickly prototype content at lower sizes before generating at full resolution—all with the same model.
[图片]
[图片]
Improved framing and composition
We empirically find that training on videos at their native aspect ratios improves composition and framing. We compare Sora against a version of our model that crops all training videos to be square, which is common practice when training generative models. The model trained on square crops (left) sometimes generates videos where the subject is only partially in view. In comparison, videos from Sora (right) have improved framing.
[图片]
[图片]
Language understanding
Training text-to-video generation systems requires a large amount of videos with corresponding text captions. We apply the re-captioning technique introduced in DALL·E 3(30) to videos. We first train a highly descriptive captioner model and then use it to produce text captions for all videos in our training set. We find that training on highly descriptive video captions improves text fidelity as well as the overall quality of videos.
Similar to DALL·E 3, we also leverage GPT to turn short user prompts into longer detailed captions that are sent to the video model. This enables Sora to generate high quality videos that accurately follow user prompts.
[图片]
Prompting with images and videos
All of the results above and in our landing page show text-to-video samples. But Sora can also be prompted with other inputs, such as pre-existing images or video. This capability enables Sora to perform a wide range of image and video editing tasks—creating perfectly looping video, animating static images, extending videos forwards or backwards in time, etc.
Animating DALL·E images
Sora is capable of generating videos provided an image and prompt as input. Below we show example videos generated based on DALL·E 2(31) and DALL·E 3(30) images.
[图片]
[图片]
[图片]
[图片]
[图片]
[图片]
Extending generated videos
Sora is also capable of extending videos, either forward or backward in time. Below are four videos that were all extended backward in time starting from a segment of a generated video. As a result, each of the four videos starts different from the others, yet all four videos lead to the same ending.
[图片]
[图片]
[图片]
We can use this method to extend a video both forward and backward to produce a seamless infinite loop.
[图片]
Video-to-video editing
Diffusion models have enabled a plethora of methods for editing images and videos from text prompts. Below we apply one of these methods, SDEdit,(32) to Sora. This technique enables Sora to transform the styles and environments of input videos zero-shot.
[图片]
[图片]
Connecting videos
We can also use Sora to gradually interpolate between two input videos, creating seamless transitions between videos with entirely different subjects and scene compositions. In the examples below, the videos in the center interpolate between the corresponding videos on the left and right.
Image generation capabilities
Sora is also capable of generating images. We do this by arranging patches of Gaussian noise in a spatial grid with a temporal extent of one frame. The model can generate images of variable sizes—up to 2048x2048 resolution.
[图片]
[图片]
[图片]
[图片]
Emerging simulation capabilities
We find that video models exhibit a number of interesting emergent capabilities when trained at scale. These capabilities enable Sora to simulate some aspects of people, animals and environments from the physical world. These properties emerge without any explicit inductive biases for 3D, objects, etc.—they are purely phenomena of scale.
3D consistency. Sora can generate videos with dynamic camera motion. As the camera shifts and rotates, people and scene elements move consistently through three-dimensional space.
[图片]
[图片]
Long-range coherence and object permanence. A significant challenge for video generation systems has been maintaining temporal consistency when sampling long videos. We find that Sora is often, though not always, able to effectively model both short- and long-range dependencies. For example, our model can persist people, animals and objects even when they are occluded or leave the frame. Likewise, it can generate multiple shots of the same character in a single sample, maintaining their appearance throughout the video.
[图片]
[图片]
Interacting with the world. Sora can sometimes simulate actions that affect the state of the world in simple ways. For example, a painter can leave new strokes along a canvas that persist over time, or a man can eat a burger and leave bite marks.
[图片]
Simulating digital worlds. Sora is also able to simulate artificial processes–one example is video games. Sora can simultaneously control the player in Minecraft with a basic policy while also rendering the world and its dynamics in high fidelity. These capabilities can be elicited zero-shot by prompting Sora with captions mentioning “Minecraft.”
[图片]
[图片]
These capabilities suggest that continued scaling of video models is a promising path towards the development of highly-capable simulators of the physical and digital world, and the objects, animals and people that live within them.
Discussion
[图片]
Sora currently exhibits numerous limitations as a simulator. For example, it does not accurately model the physics of many basic interactions, like glass shattering. Other interactions, like eating food, do not always yield correct changes in object state. We enumerate other common failure modes of the model—such as incoherencies that develop in long duration samples or spontaneous appearances of objects—in our landing page.
[图片]
We believe the capabilities Sora has today demonstrate that continued scaling of video models is a promising path towards the development of capable simulators of the physical and digital world, and the objects, animals and people that live within them.
References
1. Srivastava, Nitish, Elman Mansimov, and Ruslan Salakhudinov. "Unsupervised learning of video representations using lstms." International conference on machine learning. PMLR, 2015.
2. Chiappa, Silvia, et al. "Recurrent environment simulators." arXiv preprint arXiv:1704.02254 (2017).
3. Ha, David, and Jürgen Schmidhuber. "World models." arXiv preprint arXiv:1803.10122 (2018).
4. Vondrick, Carl, Hamed Pirsiavash, and Antonio Torralba. "Generating videos with scene dynamics." Advances in neural information processing systems 29 (2016).
5. Tulyakov, Sergey, et al. "Mocogan: Decomposing motion and content for video generation." Proceedings of the IEEE conference on computer vision and pattern recognition. 2018.
6. Clark, Aidan, Jeff Donahue, and Karen Simonyan. "Adversarial video generation on complex datasets." arXiv preprint arXiv:1907.06571 (2019).
7. Brooks, Tim, et al. "Generating long videos of dynamic scenes." Advances in Neural Information Processing Systems 35 (2022): 31769-31781.
8. Yan, Wilson, et al. "Videogpt: Video generation using vq-vae and transformers." arXiv preprint arXiv:2104.10157 (2021).
9. Wu, Chenfei, et al. "Nüwa: Visual synthesis pre-training for neural visual world creation." European conference on computer vision. Cham: Springer Nature Switzerland, 2022.
10. Ho, Jonathan, et al. "Imagen video: High definition video generation with diffusion models." arXiv preprint arXiv:2210.02303 (2022).
11. Blattmann, Andreas, et al. "Align your latents: High-resolution video synthesis with latent diffusion models." Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2023.
12. Gupta, Agrim, et al. "Photorealistic video generation with diffusion models." arXiv preprint arXiv:2312.06662 (2023).
13. Vaswani, Ashish, et al. "Attention is all you need." Advances in neural information processing systems 30 (2017).
14. Brown, Tom, et al. "Language models are few-shot learners." Advances in neural information processing systems 33 (2020): 1877-1901.
15. Dosovitskiy, Alexey, et al. "An image is worth 16x16 words: Transformers for image recognition at scale." arXiv preprint arXiv:2010.11929 (2020).
16. Arnab, Anurag, et al. "Vivit: A video vision transformer." Proceedings of the IEEE/CVF international conference on computer vision. 2021.
17. He, Kaiming, et al. "Masked autoencoders are scalable vision learners." Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 2022.
18. Dehghani, Mostafa, et al. "Patch n'Pack: NaViT, a Vision Transformer for any Aspect Ratio and Resolution." arXiv preprint arXiv:2307.06304 (2023).
19. Rombach, Robin, et al. "High-resolution image synthesis with latent diffusion models." Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 2022.
20. Kingma, Diederik P., and Max Welling. "Auto-encoding variational bayes." arXiv preprint arXiv:1312.6114 (2013).
21. Sohl-Dickstein, Jascha, et al. "Deep unsupervised learning using nonequilibrium thermodynamics." International conference on machine learning. PMLR, 2015.
22. Ho, Jonathan, Ajay Jain, and Pieter Abbeel. "Denoising diffusion probabilistic models." Advances in neural information processing systems 33 (2020): 6840-6851.
23. Nichol, Alexander Quinn, and Prafulla Dhariwal. "Improved denoising diffusion probabilistic models." International Conference on Machine Learning. PMLR, 2021.
24. Dhariwal, Prafulla, and Alexander Quinn Nichol. "Diffusion Models Beat GANs on Image Synthesis." Advances in Neural Information Processing Systems. 2021.
25. Karras, Tero, et al. "Elucidating the design space of diffusion-based generative models." Advances in Neural Information Processing Systems 35 (2022): 26565-26577.
26. Peebles, William, and Saining Xie. "Scalable diffusion models with transformers." Proceedings of the IEEE/CVF International Conference on Computer Vision. 2023.
27. Chen, Mark, et al. "Generative pretraining from pixels." International conference on machine learning. PMLR, 2020.
28. Ramesh, Aditya, et al. "Zero-shot text-to-image generation." International Conference on Machine Learning. PMLR, 2021.
29. Yu, Jiahui, et al. "Scaling autoregressive models for content-rich text-to-image generation." arXiv preprint arXiv:2206.10789 2.3 (2022): 5.
30. Betker, James, et al. "Improving image generation with better captions." Computer Science. https://cdn.openai.com/papers/dall-e-3. pdf 2.3 (2023): 8
31. Ramesh, Aditya, et al. "Hierarchical text-conditional image generation with clip latents." arXiv preprint arXiv:2204.06125 1.2 (2022): 3.
32. Meng, Chenlin, et al. "Sdedit: Guided image synthesis and editing with stochastic differential equations." arXiv preprint arXiv:2108.01073 (2021).