# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

iris = pd.read_csv('./iris.csv')
dummy = pd.get_dummies(iris['species'])  # 对Species生成哑变量

iris = pd.concat([iris, dummy], axis=1)

X = iris.ix[:, 0:4]
Y = iris['setosa'].reshape(len(iris), 1)  # 整理出X矩阵和Y矩阵


def GDA(Y, X):
    # 得到Y分布的theta向量
    theta1 = Y.mean()  # 类别1的比例
    theta0 = 1 - Y.mean()  # 类别2的比例

    mu1 = X[Y == 1].mean()  # 类别1特征的均值向量
    mu0 = X[Y == 0].mean()  # 类别2特征的均值向量

    X_1 = X[Y == 1]
    X_0 = X[Y == 0]

    # sigma = X.T * X - n * (X.bar).T * X.bar，将sigma的式子展开就得到这个，这里分别算出两类的sigma求和除以总样本个数m
    A = np.dot(X_1.T, X_1) - len(Y[Y == 1]) * np.dot(mu1.reshape(4, 1), mu1.reshape(4, 1).T)
    B = np.dot(X_0.T, X_0) - len(Y[Y == 0]) * np.dot(mu0.reshape(4, 1), mu0.reshape(4, 1).T)
    sigma = (A + B) / len(X)
    return dict({'theta1': theta1,
                 'theta0': theta0,
                 'mu1': mu1,
                 'mu0': mu0,
                 'sigma': sigma
                 })


print GDA(Y, X)
