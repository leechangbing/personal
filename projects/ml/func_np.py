import numpy as np

# 测试多维数组
def test_ndarray():
    a = np.array([1, 2, 3, 4], dtype=np.int32)
    print(a)
    b = np.array([[1, 2], [3, 4]], dtype=np.float32)
    print(b)
    print(np.zeros((2, 3), dtype=np.int32))
    print(np.ones((2, 3), dtype=np.int32))
    print(np.full((2, 3), 4, dtype=np.int32))
    print(np.arange(0, 10, 2, dtype=np.int32))
    print(np.linspace(0, 10, 2, dtype=np.int32))
    print(np.eye(3, dtype=np.int32))

# 测试数组属性
def test_ndarray_attribute():
   a = np.array([[1,2,3],[4,5,6,]], dtype=np.int32)
   print(a)
   print(a.shape)  # 形状
   print(a.ndim) # 维度
   print(a.size) # 元素数量
   print(a.dtype) # 数据类型


# 测试数组操作
def test_ndarray_operation():
    a = np.array([[1,2,3],[4,5,6,]], dtype=np.int32)
    # 切片与索引
    print(a[0,1]) # 指定元素
    print(a[:,1]) # 第二列
    # 重塑
    b = a.reshape((3,2))
    print(b)
    # 广播
    c = a + 10
    print(c)


# 测试数组计算
def test_ndarray_compute():

    # 按照元素计算
    a = np.array([1,2,3])
    b = np.array([4,5,6])
    print(a + b)
    print(a * b)

    # 聚合函数
    print(np.sum(a))
    print(np.mean(a))
    print(np.std(a))
    print(np.max(a), np.min(a))


# 测试随机数生成
def test_random():
    print(np.random.seed(42))  # 设置随机种子
    print(np.random.rand(2,2)) # [0,1)均匀分布
    print(np.random.randn(2,2)) # 标准正太分布
    print(np.random.randint(0,10,2)) # 0~9之间的2个整数


if __name__ == '__main__':
    test_ndarray() # 测试多维数组

    test_ndarray_attribute() # 测试数组属性

    test_ndarray_operation() # 测试数组操作

    test_ndarray_compute() # 测试数组计算

    test_random() # 随机数测试


    print("test finished!")


