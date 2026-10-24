
论文地址：An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale
解读地址：详解VIT(Vision Transformer)模型原理, 代码级讲解_vit模型-CSDN博客
模型简介
论文地位：VIT模型（version transformer），这一篇Google于2021年发表在计算机视觉顶级会议ICLR上的一篇文章。它首次将Transformer这种源于NLP领域中的模型引入到CV领域，并在imagenet数据集中击败当时最先进的CNN模型。这是一个标志性的网络，代表transformer击败了CNN和RNN，同时在CV领域和NLP领域达到了统治地位，伺候基本在ImageNet排行榜上都是基于transformer机构的模型了。
整体架构介绍
VIT首次将transformer模型运用在CV领域并且取得了不错的分类效果，模型原理如下图所示，可以看出VIT只用了transformer模型的编码器部分，并未涉及解码器。其实VIT模型不难理解，只需要将其拆分为三个部分：1. 图像特征嵌入模块；2. transformer编码器部分；3. MLP分类模块。
图像嵌入模块
标准的VIT模型对图像的输入尺寸有要求，必须为224*224. 图像输入之后首先进行patch分块，一般设置patch为16*16，那么一共能生成(224/16) * (224/16) = 196个patch块。这一部分如何实现呢？用一个卷积层就可以实现，其卷积核大小为patch size=16，步长为patch size=16。
具体代码如下所示：每行代码均有详细注释，展示了图像分块和特征嵌入的完整过程，嵌入之后的特征维度[196, 768]，之后我们还需要加上位置编码和类token，前者使用直接相加的方法，后者使用concat的方法，所以加上类别token后，特征的维度变化为[197, 768]。
Transformer Encoder
主要由LayerNorm层，多头注意力机制，MLP模块，残差链接这5个模块组成。这是整个VIT模型最重要也是最需要花费精力理解的地方。
class Attention(nn.Module):
    #经过注意力层的输入和输出维度相同
    def 
__init__
(self,
                 dim,
                 num_heads = 8,
                 qkv_bias = False,
                 qk_scale = None,
                 attn_drop_ratio = 0.,
                 proj_drop_ratio = 0.):
        super(Attention, self).
__init__
()
        self.num_heads = num_heads
        head_dim = dim // num_heads
        self.scale = qk_scale or head_dim ** -0.5
        self.qkv = nn.Linear(dim, dim * 3, bias = qkv_bias)
        self.attn_drop = nn.Dropout(attn_drop_ratio)
        self.proj = nn.Linear(dim, dim)
        self.proj_drop = nn.Dropout(proj_drop_ratio)

     def forward(self, x):
          B, N, C = x.shape
          qkv = self.qkv(x).reshape(B, N, 3, self.num_heads,
然后是MLP模块，也就是transformer原文中的前馈网络(feed forward)，这一部分其实比较简单，就是两个全连接层加上dropout层实现。
class MLP(nn.Module):
    """
    MLP as used in Vision Transformer, MLP-Mixer and related networks.
    """
    def 
__init__
(self, in_features, hidden_features=None, out_features=None, act_layer=nn.GELU, drop=0.):
        super().
__inie__
()
        out_features = out_features or in_features
        hidden_features = hidden_features or in_features
        self.fc1 = nn.Linear(in_features, hidden_features)
        self.act1 = act_layer()
        self.fc2 = nn.Linear(hidden_features, out_features)
        self.drop = nn.Dropout(drop)

    def forward(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.drop(x)
        x = self.fc2(x)
        x = self.drop(x)
        return x
残差连接模块，代码实现如下：
x = x + self.drop_path(self.attn(self.norm1(x)))
x = x + self.drop_path(self.mlp(self.norm2(x)))
剩下是将这些不同功能的模块进行包装，代码和注释如下：
class Block(nn.Module):
    #集成了Transformer Encoder的所有功能
    def 
__init__
(self,
                 dim,
                 num_heads,
                 mlp_ratio=4.,
                 qkv_bias=False,
                 drop_ratio=0..
                 attn_drop_ratio=0.,
                 drop_path_ratio=0.,
                 act_layer=nn.GELU,
                 norm_layer=nn.LayerNorm):
          super(Block, self).
__init__
()
          self.norm1 = norm_layer(dim)
          self.attn = Attention(dim, num_heads=num_heads, qkv_bias=qkv_bias, qk_scale = qk_scale,
                              attn_drop_ratio = attn_drop_ratio, proj_drop=drop_ratio)
          self.drop_path = DropPath(drop_path_ratio) if drop_path_ratio > 0. else nn.Indentity()
          self.norm2 = norm_layer(dim)
          mlp_hidden_dim = int(dim * mlp_ratio)
          self.mlp = MLP(in_features = dim, hidden_features = mlp_hidden_dim, act_layer=act_layer, drop=drop_ratio)

      def forward(self, x):
          x = x + self.drop_path(self.attn(self.norm1(x)))
          x = x + self.drop_path(self.mlp(self.norm2(x)))
          return x
接下来就是最后的MLP分类模块，这一个部分比较简单，甚至可以只用一层全连接层来解决。这里需要提示一下，输入到MLP类别分类器中的特征只有类别token，经过N层tranformer编码器处理后的特征的维度和输入钱相同，均为[197, 768]，我们只使用列别切片的方式提取出类别token，维度为[1, 768]。进行下一步的类别分类。那是不是其他的特征没有用处？浪费了是不是。其实不是，多头注意力可以让不同位置的特征进行全面交互，这里输出的类别token和之前输入的类别token早已发生了巨变，这种变化是由其它特征导致的。
class VisionTransformer(nn.Module):
    def 
__init__
():
        return None
    def forward_features(self, x):
        return None
    def forward(self, x):
        return None
