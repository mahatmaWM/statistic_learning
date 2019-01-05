# coding=utf-8

import numpy as np
import copy as cp

'''
Q是所有可能的状态的集合
V是所有可能的观测的集合
N是可能的状态数
M是可能的观测数
I是长度为T的状态序列，O是对应的观测序列
A是状态转移矩阵，N*N
B是观测概率矩阵，N*M
pi是厨师状态概率向量

隐马尔科夫模型lambda=(A,B,pi)

三个问题：
1、概率计算问题。给定模型lambda和观测序列O，计算概率p(O|lambda)
2、学习问题。给定观测序列O，估计模型lambda=(A,B,pi)参数，是的在该模型lambda下，观察序列O出现的概率最大
3、预测（解码）问题。已知模型lambda和观测序列O，求在该观测序列O的条件下p(I|O)概率最大的状态序列。

'''


class HMM:
    def __init__(self, Ann, Bnm, pi1n):
        self.A = np.array(Ann)
        self.B = np.array(Bnm)
        self.pi = np.array(pi1n)
        self.N = self.A.shape[1]
        self.M = self.B.shape[1]

    def printhmm(self):
        print "=================================================="
        print "HMM content: N =", self.N, ",M =", self.M
        print "A ", self.A
        print "B ", self.B
        print "hmm.pi", self.pi
        print "=================================================="

    def Forward(self, T, O, alpha):
        '''
        前向算法估计观测序列的概率，算法10.2
        :param T: 观察值序列的长度
        :param O: 观察值序列
        :param alpha: 运算中用到的临时数组
        :return: 返回值,所要求的概率
        '''
        # 1.初始化
        for i in range(self.N):
            alpha[0, i] = self.pi[i] * self.B[i, O[0]]

        # 2.递推
        for t in range(T - 1):
            for j in range(self.N):
                sum = 0.0
                for i in range(self.N):
                    sum += alpha[t, i] * self.A[i, j]
                alpha[t + 1, j] = sum * self.B[j, O[t + 1]]
        # 3.终止
        prob = 0
        for i in range(self.N):
            prob += alpha[T - 1, i]
        return prob

    def Backward(self, T, O, beta):
        '''
        后向算法
        :param T: 观察值序列的长度，算法10.3
        :param O: 观察值序列
        :param beta: 运算中用到的临时数组
        :return: 返回值，所要求的概率
        '''
        # 1. Intialization
        for i in range(self.N):
            beta[T - 1, i] = 1.0
        # 2. Induction
        for t in range(T - 2, -1, -1):
            for i in range(self.N):
                sum = 0.0
                for j in range(self.N):
                    sum += self.A[i, j] * self.B[j, O[t + 1]] * beta[t + 1, j]
                beta[t, i] = sum

        # 3. Termination
        pprob = 0.0
        for i in range(self.N):
            pprob += self.pi[i] * self.B[i, O[0]] * beta[0, i]
        return pprob

    def viterbi(self, O):
        '''
        预测解码的viterbi算法，对应185页算法10.5
        :param O: 观察序列
        :return: P(O|lambda)最大时的最优状态路径I
        '''
        T = len(O)
        # 初始化
        delta = np.zeros((T, self.N), np.float)
        phi = np.zeros((T, self.N), np.float)
        I = np.zeros(T)
        for i in range(self.N):
            delta[0, i] = self.pi[i] * self.B[i, O[0]]
            phi[0, i] = 0

        # 递推
        # np.argmax()最大元素的索引
        for t in range(1, T):
            for i in range(self.N):
                delta[t, i] = self.B[i, O[t]] * np.array([delta[t - 1, j] * self.A[j, i] for j in range(self.N)]).max()
                phi[t, i] = np.array([delta[t - 1, j] * self.A[j, i] for j in range(self.N)]).argmax()

        # 终结
        prob = delta[T - 1, :].max()
        I[T - 1] = delta[T - 1, :].argmax()

        # 状态序列求取
        for t in range(T - 2, -1, -1):
            I[t] = phi[t + 1, int(I[t + 1])]
        return I, prob

    def ComputeGamma(self, T, alpha, beta, gamma):
        '''
        对应公式10.24
        :param T:
        :param alpha:
        :param beta:
        :param gamma:
        :return:
        '''
        for t in range(T):
            denominator = 0.0
            for j in range(self.N):
                gamma[t, j] = alpha[t, j] * beta[t, j]
                denominator += gamma[t, j]
            for i in range(self.N):
                gamma[t, i] = gamma[t, i] / denominator

    def ComputeXi(self, T, O, alpha, beta, xi):
        '''
        对应公式10.26
        :param T:
        :param O:
        :param alpha:
        :param beta:
        :param xi:
        :return:
        '''
        for t in range(T - 1):
            sum = 0.0
            for i in range(self.N):
                for j in range(self.N):
                    xi[t, i, j] = alpha[t, i] * beta[t + 1, j] * self.A[i, j] * self.B[j, O[t + 1]]
                    sum += xi[t, i, j]
            for i in range(self.N):
                for j in range(self.N):
                    xi[t, i, j] /= sum

    def BaumWelch(self, S, T, O, alpha, beta, gamma, iterate=5000):
        '''
        输入S个长度为T的观察序列O
        :param S:
        :param T:
        :param O:
        :param alpha:
        :param beta:
        :param gamma:
        :param iterate:
        :return: 初始模型：HMM={A,B,pi,N,M}
        '''
        DELTA = 0.000000000000001
        round = 0
        oldpi = cp.deepcopy(self.pi)
        oldA = cp.deepcopy(self.A)
        oldB = cp.deepcopy(self.B)

        xi = np.zeros((T, self.N, self.N), np.float)
        pi = np.zeros(T, np.float)
        denominatorA = np.zeros(self.N, np.float)
        denominatorB = np.zeros(self.N, np.float)
        numeratorA = np.zeros([self.N, self.N], np.float)
        numeratorB = np.zeros([self.N, self.M], np.float)

        while round < iterate:
            round += 1
            # E step
            for l in range(S):
                _ = max(self.Forward(T, O[l], alpha), self.Backward(T, O[l], beta))
                self.ComputeGamma(T, alpha, beta, gamma)
                self.ComputeXi(T, O[l], alpha, beta, xi)
                for i in range(self.N):
                    pi[i] += gamma[0, i]
                    for t in range(T - 1):
                        denominatorA[i] += gamma[t, i]
                        denominatorB[i] += gamma[t, i]
                    denominatorB[i] += gamma[T - 1, i]

                    for j in range(self.N):
                        for t in range(T - 1):
                            numeratorA[i, j] += xi[t, i, j]

                    for k in range(self.M):
                        for t in range(T):
                            if O[l][t] == k:
                                numeratorB[i, k] += gamma[t, i]

            # M step 重估状态转移矩阵、观察概率矩阵
            a = 0.001  # 教材里面a=0，没有考虑平滑
            b = 1 - a
            for i in range(self.N):
                self.pi[i] = a / self.N + b * pi[i] / S
                for j in range(self.N):
                    self.A[i, j] = a / self.N + b * numeratorA[i, j] / denominatorA[i]
                    numeratorA[i, j] = 0.0
                for k in range(self.M):
                    self.B[i, k] = a / self.M + b * numeratorB[i, k] / denominatorB[i]
                    numeratorB[i, k] = 0.0
                pi[i] = denominatorA[i] = denominatorB[i] = 0.0

            # 检查参数是否到达阈值条件
            diff_pi_max = np.max(abs(self.pi - oldpi))
            diff_A_max = np.max(abs(self.A - oldA))
            diff_B_max = np.max(abs(self.B - oldB))
            temp = np.max([diff_A_max, diff_B_max, diff_pi_max])
            if temp <= DELTA:
                print "num iteration ", round
                break
            else:
                oldpi = cp.deepcopy(self.pi)
                oldA = cp.deepcopy(self.A)
                oldB = cp.deepcopy(self.B)


if __name__ == "__main__":
    # page 177例子
    A = np.array([[0.5, 0.2, 0.3],
                  [0.3, 0.5, 0.2],
                  [0.2, 0.3, 0.5]])
    B = np.array([[0.5, 0.5],
                  [0.4, 0.6],
                  [0.7, 0.3]])
    pi = [0.2, 0.4, 0.4]
    hmm = HMM(A, B, pi)

    O = np.array([0, 1, 0])
    T = 3
    alpha = np.zeros((T, hmm.N), np.float)
    prob = hmm.Forward(T, O, alpha)
    print 'forward ', prob

    beta = np.zeros((T, hmm.N), np.float)
    prob = hmm.Backward(T, O, beta)
    print 'backward ', prob

    I, prob = hmm.viterbi(O)
    print I, prob

    # gusse the prarameter of HMM
    A = np.array([[0.5, 0.2, 0.3],
                  [0.3, 0.5, 0.2],
                  [0.2, 0.3, 0.5]])
    B = np.array([[0.5, 0.5],
                  [0.4, 0.6],
                  [0.7, 0.3]])
    pi = [0.2, 0.4, 0.4]
    hmm = HMM(A, B, pi)

    O = [[0, 1, 0]]
    S = 1
    T = 3

    alpha = np.zeros((T, hmm.N), np.float)
    beta = np.zeros((T, hmm.N), np.float)
    gamma = np.zeros((T, hmm.N), np.float)
    hmm.BaumWelch(S, T, O, alpha, beta, gamma)
    hmm.printhmm()
