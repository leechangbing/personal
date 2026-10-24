import numpy as np
import pandas as pd

n = 10000
d = 5
r = 0.01


def linear_train(x, y):
    w = np.random.normal(0, 1, (d, ))
    print(w.shape)
    for i in range(100):
        y_hat = np.dot(X, w)
        loss = np.sum((y_hat - y) * (y_hat - y)) / n
        gd = np.dot((y_hat-y), x)/n
        w -= gd*r
        print("第{}, loss:{}".format(i, loss))
        print(w)


def logistic_train(x, y):
    r = 0.1
    w = np.random.normal(0, 1, (d, ))
    print(w.shape)
    for i in range(1000):
        y_hat = np.dot(X, w)
        y_hat = 1/(1+np.exp(-y_hat))
        loss = np.sum(y * np.log(y_hat)) / n
        gd = np.dot(y*(y_hat-1), x)/n
        w -= gd*r
        print("第{}, loss:{}".format(i, loss))
        print(w)
        print(gd)


if __name__ == "__main__":
    X = np.random.randn(n, d) * 10
    W = np.array([0.1, 0.2, 0.3, 0.4, 0.5]) * 10
    Y = np.dot(X, W)
    Yc = 1/(1+np.exp(-Y))
    Yc = (Yc > 0.5).astype(int)

    linear_train(X, Y)
    logistic_train(X, Yc)


