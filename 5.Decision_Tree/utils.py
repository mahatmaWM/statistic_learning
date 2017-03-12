# coding=utf-8
import pandas as pd
import numpy as np


def createDataSet():
    data = pd.read_csv("data.csv", sep=',', dtype='str')
    df = pd.DataFrame(data)
    df.columns = ['outlook', 'temperature', 'humidity', 'windy', 'label']
    labels = df.columns[:-1].values
    # 将字符串映射成数字，numpy才好处理
    mapping1 = {label: idx for idx, label in enumerate(np.unique(df['outlook']))}
    df['outlook'] = df['outlook'].map(mapping1)
    mapping2 = {label: idx for idx, label in enumerate(np.unique(df['temperature']))}
    df['temperature'] = df['temperature'].map(mapping2)
    mapping3 = {label: idx for idx, label in enumerate(np.unique(df['humidity']))}
    df['humidity'] = df['humidity'].map(mapping3)
    mapping4 = {label: idx for idx, label in enumerate(np.unique(df['windy']))}
    df['windy'] = df['windy'].map(mapping4)
    dataSet = df[['outlook', 'temperature', 'humidity', 'windy', 'label']].values
    return dataSet, labels


from math import log


def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 1
        else:
            labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt


def splitDataSet(dataSet, feature, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[feature] == value:
            index = []
            index.append(feature)
            featVec1 = np.delete(featVec, index)  # 删除第axis个feature维度值为value的变量
            retDataSet.append(featVec1)
    return retDataSet


# 开始测试
dataSet, labels = createDataSet()
print calcShannonEnt(dataSet)
