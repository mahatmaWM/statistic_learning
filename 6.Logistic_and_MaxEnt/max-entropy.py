# coding=utf8
import math, copy
from collections import defaultdict


class MaxEnt:
    def __init__(self):
        self._C = 0  # 样本最大的特征数量,用于求参数时的迭代，见IIS原理说明
        self._EPS = 0.01  # 判断是否收敛的阈值

        self._samples = []  # 样本集,元素是[y,x1,x2,...,xm]的元组,每行有m个特征
        self._Y = set([])  # 标签集合,相当于去重之后的y
        self._N = 0  # 样本数量
        self._n = 0  # 特征对(x_m,y_i)总数量，每个样本的每一维特征x_m与y_i组成的特征对，默认了特征之间无相关性
        self._xy_counts = defaultdict(int)  # Key是(x_m,y_i)对，Value是出现次数，记录每个样本每一维特征x_m与y_i的出现次数
        self._xy_index = defaultdict(int)  # 对特征对(xm,yi)做的顺序编号(Index),Key是(xm,yi),Value是下标,记录此特征对在期望以及权值中的位置

        self._yangben_expectation = []  # 样本分布的特征期望值
        self._moxing_expectation = []  # 模型分布的特征期望值

        self._curr_w = []  # 对应n个特征对的权值
        self._pre_w = []

    def load_data(self, filename):
        for line in open(filename, "r"):
            sample = line.strip().split("\t")
            if len(sample) < 2:  # 输入是：标签 + 一个特征（有的样本特征数目太少，则模型假定缺失的特征平均最好）
                continue
            y = sample[0]
            X = sample[1:]

            self._samples.append(sample)  # label + features
            self._Y.add(y)
            for x in set(X):  # set对特征Xi去重
                self._xy_counts[(x, y)] += 1

    def _initparams(self):
        self._N = len(self._samples)
        self._n = len(self._xy_counts)
        self._C = max([len(sample) - 1 for sample in self._samples])
        self._curr_w = [0.0] * self._n
        self._pre_w = copy.deepcopy(self._curr_w)
        self._sample_expectation()

    def _convergence(self):
        for w, lw in zip(self._curr_w, self._pre_w):
            if math.fabs(w - lw) >= self._EPS:
                return False
        return True

    # 计算每个样本的期望并存好
    def _sample_expectation(self):
        self._yangben_expectation = [0.0] * self._n
        for i, xy in enumerate(self._xy_counts):
            self._yangben_expectation[i] = self._xy_counts[xy] * 1.0 / self._N
            self._xy_index[xy] = i

    # 作为归一化的分母
    def _zx(self, X):
        ZX = 0.0
        for y in self._Y:
            sum = 0.0
            for x in X:
                if (x, y) in self._xy_counts:
                    sum += self._curr_w[self._xy_index[(x, y)]] * self._yangben_expectation[self._xy_index[(x, y)]]
            ZX += math.exp(sum)
        return ZX

    # 条件概率p(y|x)的计算，每一轮迭代都要重新计算
    def _pyx(self, X):
        ZX = self._zx(X)
        results = []
        for y in self._Y:
            sum = 0.0
            for x in X:
                if (x, y) in self._xy_counts:
                    sum += self._curr_w[self._xy_index[(x, y)]] * self._yangben_expectation[self._xy_index[(x, y)]]
            pyx = 1.0 / ZX * math.exp(sum)
            results.append((y, pyx))
        return results

    # 模型的期望，每一轮迭代都要重新计算
    def _model_expectation(self):
        self._moxing_expectation = [0.0] * self._n
        for sample in self._samples:
            X = sample[1:]
            pyx = self._pyx(X)
            for y, p in pyx:
                # print '_model_expectation','y', y, 'p', p
                for x in X:
                    if (x, y) in self._xy_counts:
                        self._moxing_expectation[self._xy_index[(x, y)]] += p * self._yangben_expectation[
                            self._xy_index[(x, y)]] * 1.0 / self._N

    def train(self, maxiter=1000):
        self._initparams()
        # print self._N, self._n, self._C, self._w, self._lw, self._mx_ep

        for i in range(0, maxiter):
            # print "Iter:%d..." % i
            self._pre_w = copy.deepcopy(self._curr_w)
            # 计算新一轮模型的期望
            self._model_expectation()
            # 更新每个特征的权值
            for i, w in enumerate(self._curr_w):
                self._curr_w[i] += 1.0 / self._C * math.log(self._yangben_expectation[i] / self._moxing_expectation[i])
            # print self._w
            # 检查是否收敛
            if self._convergence():
                break

    def predict(self, input):
        X = input.strip().split("\t")
        prob = self._pyx(X)
        return prob


if __name__ == "__main__":
    maxent = MaxEnt()
    maxent.load_data('data.txt')
    maxent.train()
    print maxent.predict("sunny\thot\thigh\tFALSE")
    print maxent.predict("overcast\thot\thigh\tFALSE")
    print maxent.predict("sunny\tcool\thigh\tTRUE")
