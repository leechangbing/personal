# Markdown 标题语法
参考链接：https://markdown.com.cn/


# 一级标题
## 二级标题
### 三级标题

# Markdown 段落语法
要创建段落，使用空白行或者多行文本行进行分隔。

I really like using Markdown.

I think I'll use it to format all of my documents from now on.

# Markdown 换行语法
在一行的末尾添加两个或者多个空格，然后按回车键，即可创建一个换行 <br>

This is the first line.<br>
And This is the second line.

This is the first line.  
And This is the second line.

# Markdown 强调语法

## 粗体（Bold）
要加粗体，在单词前后各加两个星号和下划线。如果需要加粗一个单词或者短语的中间部分以示强调的话，在加粗部分前后各加两个星号。  
__a__<br>
**a**<br>
I'm **fine** 

##  斜体（Italic）
在单词或者短语前后各添加一个星号或者下划线，要斜体突出单词的部分，请在字母前后各添加一个星号，中间不要带空格。  
*ABC*  
A*cat*meow

## 粗体(Bold)和斜体(Italic)
要同时用粗体和斜体突出显示文本，在单词或者短语的前后各添加三个星号或者下划线。  
A***cat***meow


# Markdown 引用语法
要创建块引用，在段落前添加一个>号。
> 创建引用信息   
> 你好
>

## 多行引用
> 创建引用信息 
>
> 你好


## 嵌套引用
> 创建引用信息 
>
> >你好


# Markdown列表语法

## 有序列表
1. 一级
2. 二级

## 无序列表
- 一级
- 二级

# Markdown代码语法
要将单词或者短语表示为代码，请将其包裹在反引号`中。

## 转义反引号

如果你要表示为代码的单词或者短语中包含一个或者多个反引号


## 代码块
将代码块的每行缩紧至少四个空白格，或者一个制表符；

    #include<iostream>
    int main(){

        return 
    }


# Markdown 分隔符语法

要创建分隔符，请在单独一行上使用三个或者多个星号（****）、破折号（----）或者下划线（___），并且不能包含其它内容。


----
测试1
****
测试2
___
测试3



# Markdown 链接语法

链接文本放在中括号内，链接地址放在后面的括号中，链接title可选:  
这是一个链接[Markdown语法](https://markdown.com.cn "最好的markdown教程")  
这是一个网站[百度](https://www.baidu.com "百度一下")

## 网址和Email地址
使用简括号<>可以很方便地将URL或者email地址变成可以点击的链接。

<https://markdown.com.cn>  
<fake@example.com>

## 带格式化的链接

I love supporting the **[EFF](https://eff.org)**.
This is the *[Markdown Guide](https://www.markdownguide.org)*.
See the section on [`code`](#code).


# Markdown 图片语法

要添加图像，请使用感叹号（!），然后在放括号增加替代文本，图片链接放在圆括号中，括号里的链接后可以增加一个可选的图片标题文本。

![这是图片](/assets/img/philly-magic-garden.jpg "Magic Gardens")



