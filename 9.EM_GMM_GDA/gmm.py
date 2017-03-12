# -*- coding: utf-8 -*-

import copy
import math
import numpy as np
import matplotlib.pyplot as plt

isdebug = True
np.random.seed(1234)


# 指定k个高斯分布参数，这里指定k=2。注意2个高斯分布具有相同均方差Sigma，分别为Mu1,Mu2。
def ini_data(Sigma, Mu1, Mu2, k, N):
    global X
    global Mu
    global Expectations
    X = np.zeros((1, N))
    Mu = np.random.random(2)
    Expectations = np.zeros((N, k))  # 这个矩阵就是隐变量Zik，第i个观测来自第k个分模型则为1，其余为0

    for i in xrange(0, N):  # 生成N个观察变量X，放到一维数组
        if np.random.random(1) > 0.5:
            X[0, i] = np.random.normal() * Sigma + Mu1
        else:
            X[0, i] = np.random.normal() * Sigma + Mu2
    if isdebug:
        print "***********"
        print "初始观测数据X："
        print X


# EM算法：步骤1，计算E[Zij]
def e_step(Sigma, k, N):
    global Expectations
    global Mu
    global X
    # 对每一个观察样本
    for i in xrange(0, N):
        Denom = 0
        # 以下两个for是为了计算N*K的隐变量矩阵，这个矩阵叫响应概率矩阵，代表每个观测样本属于每个分布的概率记录
        for j in xrange(0, k):
            # 高斯分布公式
            Denom += (1 / math.sqrt(2 * math.pi)) * math.exp(
                (-1 / (2 * (float(Sigma ** 2)))) * (float(X[0, i] - Mu[j])) ** 2)
        for j in xrange(0, k):
            Numer = (1 / math.sqrt(2 * math.pi)) * math.exp(
                (-1 / (2 * (float(Sigma ** 2)))) * (float(X[0, i] - Mu[j])) ** 2)
            Expectations[i, j] = Numer / Denom
    if isdebug:
        print "***********"
        print "隐藏变量E（Z）:"
        print Expectations


# EM算法：步骤2，求最大化E[zij]的参数Mu
def m_step(k, N):
    global Expectations
    global X
    for j in xrange(0, k):
        Numer = 0
        Denom = 0
        for i in xrange(0, N):
            Numer += Expectations[i, j] * X[0, i]
            Denom += Expectations[i, j]
        Mu[j] = Numer / Denom


# 算法迭代iter_num次，或达到精度Epsilon停止迭代
def run(Sigma, Mu1, Mu2, k, N, iter_num, Epsilon):
    ini_data(Sigma, Mu1, Mu2, k, N)
    print "初始<u1,u2>:", Mu
    for i in range(iter_num):
        Old_Mu = copy.deepcopy(Mu)
        e_step(Sigma, k, N)
        m_step(k, N)
        print i, Mu
        if np.sum(np.abs(Mu - Old_Mu)) < Epsilon:
            break


if __name__ == '__main__':
    run(6, 40, 20, 2, 1000, 1000, 0.000001)
    plt.hist(X[0, :], 50)
    plt.show()
