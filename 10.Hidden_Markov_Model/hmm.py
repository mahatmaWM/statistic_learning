# -*-coding:UTF-8-*-
import numpy as np
import copy as cp


class HMM:
    def __init__(self, Ann, Bnm, pi1n):
        self.A = np.array(Ann)
        self.B = np.array(Bnm)
        self.pi = np.array(pi1n)
        self.N = self.A.shape[0]
        self.M = self.B.shape[1]

    def printhmm(self):
        print "=================================================="
        print "HMM content: N =", self.N, ",M =", self.M
        print "A ", self.A
        print "B ", self.B
        print "hmm.pi", self.pi
        print "=================================================="

    # 函数名称：Forward
    # 功能：前向算法估计参数
    # 参数:
    # phmm:指向HMM的指针
    # T:观察值序列的长度
    # O:观察值序列
    # alpha:运算中用到的临时数组
    # pprob:返回值,所要求的概率
    def Forward(self, T, O, alpha):
        # 1.Initialization 初始化
        for i in range(self.N):
            alpha[0, i] = self.pi[i] * self.B[i, O[0]]

        # 2.Induction 递归
        for t in range(T - 1):
            for j in range(self.N):
                sum = 0.0
                for i in range(self.N):
                    sum += alpha[t, i] * self.A[i, j]
                alpha[t + 1, j] = sum * self.B[j, O[t + 1]]
        # 3.Termination 终止
        prob = 0
        for i in range(self.N):
            prob += alpha[T - 1, i]
        return prob

    # 函数名称：Backward
    # 功能:后向算法估计参数
    # 参数:phmm:指向HMM的指针
    # T:观察值序列的长度
    # O:观察值序列
    # beta:运算中用到的临时数组
    # pprob:返回值，所要求的概率
    def Backward(self, T, O, beta):
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

    # Viterbi算法
    # 输入：A，B，pi,O
    # 输出P(O|lambda)最大时Poptimal的路径I
    def viterbi(self, O):
        T = len(O)
        # 初始化
        delta = np.zeros((T, self.N), np.float)
        phi = np.zeros((T, self.N), np.float)
        I = np.zeros(T)
        for i in range(self.N):
            delta[0, i] = self.pi[i] * self.B[i, O[0]]
            phi[0, i] = 0
        # 递推
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

    # 给定模型lambda和观察O，t时刻处于状态q_i的概率，计算gamma
    def ComputeGamma(self, T, alpha, beta, gamma):
        for t in range(T):
            denominator = 0.0
            for j in range(self.N):
                gamma[t, j] = alpha[t, j] * beta[t, j]
                denominator += gamma[t, j]
            for i in range(self.N):
                gamma[t, i] = gamma[t, i] / denominator

    # 给定模型lambda和观察O，t时刻处于q_i的状态，t+1时刻处于q_j的状态的概率，计算sai(i,j)
    def ComputeXi(self, T, O, alpha, beta, xi):
        for t in range(T - 1):
            sum = 0.0
            for i in range(self.N):
                for j in range(self.N):
                    xi[t, i, j] = alpha[t, i] * beta[t + 1, j] * self.A[i, j] * self.B[j, O[t + 1]]
                    sum += xi[t, i, j]
            for i in range(self.N):
                for j in range(self.N):
                    xi[t, i, j] /= sum

    # Baum-Welch算法
    # 输入S个长度为T的观察序列O
    # 初始模型：HMM={A,B,pi,N,M}
    def BaumWelch(self, S, T, O, alpha, beta, gamma, iterate=5000):
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
            temp = np.max(np.max(np.max(abs(self.pi - oldpi)), np.max(abs(self.A - oldA))), np.max(abs(self.B - oldB)))
            print temp
            if temp <= DELTA:
                print "num iteration ", round
                break
            else:
                oldpi = cp.deepcopy(self.pi)
                oldA = cp.deepcopy(self.A)
                oldB = cp.deepcopy(self.B)


if __name__ == "__main__":
    # page 177例子
    A = np.array([[0.5, 0.2, 0.3], [0.3, 0.5, 0.2], [0.2, 0.3, 0.5]])
    B = np.array([[0.5, 0.5], [0.4, 0.6], [0.7, 0.3]])
    pi = [0.2, 0.4, 0.4]
    hmm = HMM(A, B, pi)
    O = np.array([0, 1, 0])  # 看B的行向量有几种状态
    T = 3
    alpha = np.zeros((T, hmm.N), np.float)
    prob = hmm.Forward(T, O, alpha)
    print 'forward ', prob

    beta = np.zeros((T, hmm.N), np.float)
    prob = hmm.Backward(T, O, beta)
    print 'backward ', prob

    I, prob = hmm.viterbi(O)
    print I, prob

    # gusse the prarameter of HMM, initial crf.md random value
    A = np.array([[0.5, 0.2, 0.3], [0.3, 0.5, 0.2], [0.2, 0.3, 0.5]])
    B = np.array([[0.5, 0.5], [0.4, 0.6], [0.7, 0.3]])
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
