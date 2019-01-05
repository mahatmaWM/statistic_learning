# -*- coding: utf-8 -*-
import pandas as pd
from numpy import *


def load_model(f_name):
    ifp = open(f_name, 'rb')
    return eval(ifp.read())  # eval参数是一个字符串, 可以把这个字符串当成表达式来求值,


prob_start = load_model("data/prob_start.py")
prob_emit = load_model("data/prob_emit.py")


def viterbi(obs, states, start_p, emit_p):  # 维特比算法（一种递归算法）
    """
    :param obs:分词目标句子
    :param states:状态概率
    :param start_p:发射概率
    :param trans_p:转移概率字典
    :param emit_p:定标签下，观察值概率矩阵
    :return:
    """
    alllines = []  # [{}]里面存储每一层tag和对应的最大概率值
    start = {}
    for tag in states:
        if tag in start_p.keys():
            start[tag] = start_p[tag] * emit_p[tag]["start"][obs[0]]
    alllines.append(start)
    lenght = len(obs)
    path = []  # 存储每一层的tag最大概率值对应的前一个tag
    pro = ""
    for i in range(1, lenght):
        next_dict = {}
        new_path = {}
        for static in states:
            list = []
            max = 0
            for key in alllines[i - 1].keys():
                value = alllines[i - 1][key] * emit_p[static][key][obs[i]]
                if value > max:
                    max = value
                    pro = key
                list.append(value)
            next_dict[static] = max
            new_path[static] = pro
        path.append(new_path)
        alllines.append(next_dict)
    # 寻找路径
    max = 0
    end = ""
    for key in alllines[-1].keys():
        if alllines[-1][key] > max:
            end = key
    result = []
    result.append(end)
    for i in range(len(alllines) - 2, -1, -1):
        for key in path[i].keys():
            if key == result[len(alllines) - i - 2]:
                result.append(path[i][key])
    result.reverse()
    print(result)


def cut(sentence):
    viterbi(sentence, ['B', 'M', 'E', 'S'], prob_start, prob_emit)


if __name__ == "__main__":
    test_str = u"我们是中国人。"
    cut(test_str)
