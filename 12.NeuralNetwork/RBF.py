"""
径向基神经网络的介绍见http://blog.csdn.net/zouxy09/article/details/13297881
"""
# coding=utf-8
from scipy import *
from scipy.linalg import norm, pinv
from matplotlib import pyplot as plt


class RBF:
    def __init__(self, indim, numCenters, outdim):
        self.indim = indim
        self.outdim = outdim
        self.numCenters = numCenters
        self.centers = [random.uniform(-1, 1, indim) for i in range(numCenters)]
        self.beta = 8
        self.W = random.random((self.numCenters, self.outdim))

    def _basisfunc(self, c, d):
        assert len(d) == self.indim
        return exp(-self.beta * norm(c - d) ** 2)

    def _calcAct(self, X):
        # calculate activations of RBFs
        G = zeros((X.shape[0], self.numCenters), float)
        for ci, c in enumerate(self.centers):
            for xi, x in enumerate(X):
                G[xi, ci] = self._basisfunc(c, x)
        return G

    def train(self, X, Y):
        """
        :param X:matrix of dimensions n x indim
        :param Y:y: column vector of dimension n x 1
        :return:
        """
        # 选择numCenters个径向基的中心
        rnd_idx = random.permutation(X.shape[0])[:self.numCenters]
        self.centers = [X[i, :] for i in rnd_idx]
        print("center", self.centers)

        # calculate activations of RBFs
        G = self._calcAct(X)
        print(G)

        # calculate output weights (pseudoinverse)
        self.W = dot(pinv(G), Y)

    def test(self, X):
        """
        :param X:matrix of dimensions n x indim
        :return:
        """
        G = self._calcAct(X)
        Y = dot(G, self.W)
        return Y


if __name__ == '__main__':
    n = 100
    x = mgrid[-1:1:complex(0, n)].reshape(n, 1)
    # set y and add random noise
    y = sin(3 * (x + 0.5) ** 3 - 1)
    y += random.normal(0, 0.1, y.shape)

    # rbf regression
    rbf = RBF(1, 10, 1)
    rbf.train(x, y)
    z = rbf.test(x)

    # plot original data
    plt.figure(figsize=(12, 8))
    plt.plot(x, y, 'k-')

    # plot learned model
    plt.plot(x, z, 'r-', linewidth=5)

    # plot rbfs
    plt.plot(rbf.centers, zeros(rbf.numCenters), 'gs')

    for c in rbf.centers:
        # RF prediction lines
        cx = arange(c - 0.7, c + 0.7, 0.01)
        cy = [rbf._basisfunc(array([cx_]), array([c])) for cx_ in cx]
        plt.plot(cx, cy, '-', color='gray', linewidth=0.2)

    plt.xlim(-1.2, 1.2)
    plt.show()
