import torch
import torch.nn as nn
import torch.nn.functional as F

device = torch.device('mps' if torch.mps.is_available() else 'cpu')
print(device)


# 张量计算
def test_tensor():
    # 创建张量
    x = torch.tensor([1,2,3], dtype = torch.float16)
    print(x.dtype, x.shape, x.device)
    y = x.to(torch.int).to('mps')
    print(y.dtype, y.shape, y.device)

    zeros = torch.zeros(2,3, dtype = torch.float16)
    print(zeros.dtype, zeros.shape, zeros.device)

    ones = torch.ones(2,3, dtype = torch.float16)
    print(ones.dtype, ones.shape, ones.device)

    x = torch.tensor([1,2,3], dtype = torch.float16, device = device)
    print(x.dtype, x.shape, x.device)

    rand_tensro = torch.rand(2,3, dtype = torch.float16)
    norm_tensro = torch.randn(2, 3, dtype = torch.float16)
    print(rand_tensro.dtype, rand_tensro.shape, rand_tensro.device)
    print(norm_tensro.dtype, norm_tensro.shape, norm_tensro.device)


    # 张量操作
    a = torch.tensor([1,2,3], dtype = torch.float16)
    b = torch.tensor([1,2,3], dtype = torch.float16)
    c = a+b
    d = a*b
    print(c)
    print(d)
    mat1 = torch.randn(2,3)
    mat2 = torch.randn(3,4)
    mat3 = torch.mm(mat1, mat2)
    print(mat3.shape)
    x = torch.randn(4,5)
    y = torch.reshape(x, (2, 10))
    z = x.view(2,10)
    print(x.shape, y.shape, z.shape)


# 自动微分
def test_grad():
    # 自动求导
    x = torch.tensor(2.0, requires_grad=True)
    y = x ** 2
    y.backward()
    print(x.grad)

    with torch.no_grad():
        z = x * 2
        print(z)


# 模型定义
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.linear = nn.Linear(10,1)

    def forward_v1(self,x):
        return self.linear(x)

    def __call__(self, *args, **kwargs):
        return self.forward_v1(*args, **kwargs)


if __name__ == '__main__':

    # test_tensor() # 张量测试

    # test_grad() # 梯度测试

    model = Net()
    output = model(torch.randn(5,10))
    print(output)
    print(model.__call__)
    print(model.forward_v1)