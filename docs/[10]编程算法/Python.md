1. 环境配置
2023年最新conda和pip国内镜像源
1. base环境重置：conda list --reversion 0
2. base环境安装指定版本python: conda install python=3.8
2. 常见问题
1. 标识符
  1. 由字母、数字、下划线组成，但不能以数字开头，并区分大小写，同时以下划线开头有特殊含义
  2. 单下划线开头代表不能直接访问的类属性，需要通过类提供的接口访问
  3. 双下划线开头代表类的私有成员
  4. 双下划线开头并以双下划线结尾，表示特殊方法专用标识符，例如__init__
2. 占位符
  1. %d：整数
  2. %s：字符串
  3. %f：浮点数
  4. %.3f：保留三位有效数字的小数
  5. %x：十六进制整数
3. 数据类型
1. 单变量赋值：x = a 
2. 多变量赋值：x, y = a, b
3.1 列表(list)
1. 声明：t = []
2. 内置函数：append, pop, count, clear, sort, reverse,index, remove
# 声明
t = [1,2,3]
# 尾部添加
t.append(4)
# 头部插入
t.insert(0,0)
# 尾部插入
t.insert(len(t)-1, 0)
# 列表反转
t.reverse()
# 排序
t.sort(reverse=Fasle)
# 元素计数
t.count(1)
# 赋值
t.copy()
# 清除
t.clear()
3.2 元组(tuple)
1. 声明：t = ()
2. 内置函数：count, index
# 元组声明
t = (1,3,1)
# 元素技术
t.count(1)
3.3 字典(dict)
1. 声明：t = dict()
2. 内置函数：get, pop, keys, values, items
# 声明
t = dict()

# 增加keys
t['1'] = 1
t['23'] = 2 

# 查询keys
print(t['1'])
print(t['23'])

# 删除keys
t.pop('1')

# 判断是否包含keys
print('1' in t.keys())

# 遍历keys
for k in t.keys():
    print(k)
    
# 遍历values
for v in t.values():
    print(v)

# 遍历items
for k, v in t.items():
    print(k,v)
3.4 集合(set)
1. 声明：t = set()
2. 内置函数：add, remove, intersection, intersection_update, union, union_update, difference
# 声明1
t1 = set()
# 添加元素
t1.add(1)
t1.add(2)
# 移除元素
t1.remove(1)

# 声明2
t2 = set({1,2,3})
# 交集
print(t2.intersecion(t1))
# 并集
print(t2.union(t1))
# 差集
print(t2.difference(t1))
4. 控制流程
4.1 分支结构(if else)
# 分支结构-1
if condition:
    print("condition")
   
# 分支结构-2
if condition:
    print("condition")
else:
    print("not condition")
    
# 分支结构-3
if codition1:
    print("condition1")
elif condition2:
    print("condition2")
else:
    print("not condition2")
4.2 循环结构(for)
# 循环结构-1
for i in range(10):
    print(i)

# 循环结构-2
while i<10:
    i++
    print(i)
5. 函数(function)
5.1 定义(define)
def max(x: int, y: int) -> int:
    if x > y:
        return x
    else:
        return y
5.2 调用(recall)
if  name == "__main__":
    print(max(1, 2))
6. 高级特性
6.1 切片(slice)
1. 正向索引：start:end, start缺失默认为开头，end缺失默认为结尾
2. 反向索引：尾部为-1，开头为-len()
3. 间隔索引：采用：：符号
# 列表声明
t = [1,2,3,4,5]
# 前三个
print(t[:3])
# 后三个
print(t[-3:]
# 正序间隔两个
print(t[::2])
6.2 迭代(ietration)
1. 遍历数据：for x in xx
2. 迭代对象：for ... In ...
3. 任何迭代对象都可以使用for循环，包括自定义的数据类型
t = {'a' = 1, 'b' = 2}
for k in t.keys():
    print(k, t[k])
6.3 列表生成式(list comeprehension)
1. 目标：快速生成一个列表
2. 筛选条件：if是筛选条件，后面不能跟else
3. 循环条件：for循环可以同时用于两个或多个变量循环
[x for i in range(10)]
[x for x in range(10) if x%2 == 0]
[m+n for m in "abc" for n in "xyz"]
[x if x%2==0 else -x for x in range(10)]
6.4 生成器(generator)
1. 采用惰性机制，在需要的时候生成数据以降低内存占用，并通过next()获取下一个返回值；
2. 如果生成算法比较复杂，可以通过定义函数来实现；如果包含yield关键字，则是generator而非普通函数；
# 列表表达式
lst = [x for x in range(10)]

# 生成器 
gnt = (x for x in range(10))
for x in gnt:
    print(x)

# 生成器函数
def fib(max):
    n, a, b = 0, 0, 1
    while n<max:
        yield b 
        a, b = b, a+b 
        n = n+1 
        return "done"

6.5 迭代器(iterator)
1. 可以使用for循环的对象，统称为可迭代对象(iterable)，包括集合数据类型和生成器；其中集合数据类型包括list, tuple, dict, set, str等，生成器包括生成器和带有yield的生成器函数。
2. 生成器不仅可以使用for循环迭代，也可以用next()调用下一个返回值；list, tuple, dict, set, str等是iterrable，但不是ietrator。
# 结果为false
isinstance([], iterator)

# 结果为true
isinstance((x for x in range(10), iterator)
7. 函数式编程
1. 面向过程编程：将复杂的问题分级为简单的任务，把大段代码层层拆分为函数，并通过调用解决复杂问题，函数是面向过程的基本单元。
2. 函数式编程：关心输入和输出数据之间的映射关系，其特点是函数本身作为参数传入到另一个函数，还允许返回一个函数。
7.1 map()
1. 使用方法：map(func, ietrable)
2. 输入参数：一个是iterable参数，另一个是函数
3. 处理过程：将传入的函数作用于每一个元素，并把结果作为新的iterable对象返回
4. 效果：map(func, [x1, x2, x3, ...]) = [f(x1), f(x2), f(x3), ...]
lst = [x for x in range(10)]
print(list(map(lambda x: 2*x, lst)))
7.2 reduce()
1. 使用方法：reduce(func, iterable)
2. 输入参数：一个是iterable参数，另一个是函数，其中函数包含两个输入参数
3. 处理过程：reduce把上一次处理结果和下一个元素计算
4. 效果：reduce(func, [x1, x2, x3, ...]) = f(f(f(x1), x2), x3)
from functools import reduce
lst = [x for x in range(10)]
print(reduce(lambda x, y: x+y, lst))
7.3 filter()
1. 使用方法：filter(func, iterable)
2. 输入参数：一个是iterable参数，另一个是函数，其中函数的返回值为true或者false
3. 处理过程：filter筛选出true的元素
lst = [x for x in range(10)]
print(list(filter(lambda x: True if x % 2 == 0 else False, lst)))
7.4 sorted()
1. 使用方法：sorted(iterable, *, key = None, reverse = False)，其中key定义排序，reverse=False定义升序
lst = [1, 2, 3]
print(lst, reverse = False)
print(lst, reverse = True)
7.5 lambda
1. 语法：lambda x, y, ... : (x+y)
2. 赋值给变量：f = lambda x: x*x 
def f(x):
    return lambda x: x*x
8. 面向对象编程
- 汇编语言：面向机器编程
- 高级语言：面向过程编程、面向对象编程
- 面向机器编程：指令
- 面向过程编程：函数 = 指令 + 控制
- 面向对象编程：函数 = 函数 + 数据
- 指令：简单逻辑和数学机审
- 函数：实现小型程序
- 对象：实现复杂程序
编程的一个重要原则是分工与复用，首先将系统分割成模块，再把每个模块分割为单元，然后将单元封装为模块，最后再将模块封装为系统。
面向对象编程：设计思想来源于自然界，类是一种概念或者声明，实例则是具体的实现；对象包括属性和行为，其中属性是数据，行为是函数。
类是一种对象模版，而实例是对象的实现，每个实例都有相同的方法但数据不同，即行为相同但属性不同。
数据封装：将类和属性捆绑在一起，好处是可以实现信息隐藏，符合最小权限原则。
8.1 访问权限
8.2 继承与多态
8.3 实例属性和类属性