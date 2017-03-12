# coding=utf-8

# 以下是根据李航老师的统计学习方法第二章29页的感知机算法实现的一个最简单的例子，本章还讲了其对偶形式的求解，空的时候看看。
import numpy as np


class PerceptronLH(object):
    def __init__(self, eta=0.01, n_iter=10):
        self.eta = eta
        self.n_iter = n_iter

    def fit(self, X, y):
        # 跟定w和b的初始值
        self.w0 = np.zeros(X.shape[1])
        self.b0 = 0

        self.w1 = None
        self.b1 = None

        for _ in range(self.n_iter):
            for xi, target in zip(X, y):
                print xi, target
                # 发现一个点分错了，则调整系数，将分界面向这个点靠近，以减少点到面的距离
                if target * (np.dot(xi, self.w0.T) + self.b0) <= 0:
                    self.w1 = self.w0 + self.eta * target * xi
                    self.b1 = self.b0 + self.eta * target

                    self.w0 = self.w1
                    self.b0 = self.b1
        return [self.w0, self.b0]


X = np.array([[3, 3], [4, 3], [1, 1]])
y = np.array([1, 1, -1])

ppn = PerceptronLH(eta=0.1, n_iter=10)
ppn.fit(X, y)
