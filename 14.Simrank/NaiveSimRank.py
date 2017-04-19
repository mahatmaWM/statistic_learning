# -*- coding: utf-8 -*-

import numpy
from numpy import matrix

"""
Naive SimRank
"""
with open('test/sample1.txt', 'r') as log_fp:
    logs = [log.strip() for log in log_fp.readlines()]

logs_tuple = [tuple(log.split(",")) for log in logs]

queries = list(set([log[0] for log in logs_tuple]))
ads = list(set([log[1] for log in logs_tuple]))

# 构造query与ad之间的关系矩阵，[query, ads]
graph = numpy.matrix(numpy.zeros([len(queries), len(ads)]))
for log in logs_tuple:
    query = log[0]
    ad = log[1]
    q_i = queries.index(query)
    a_j = ads.index(ad)
    graph[q_i, a_j] += 1

print graph

query_sim = matrix(numpy.identity(len(queries)))
ad_sim = matrix(numpy.identity(len(ads)))


# 计算某个query所连接的ad数目，返回一个向量组成的矩阵
def get_ads_num(query):
    q_i = queries.index(query)
    return graph[q_i]


# 计算某个ad所连接的query数目，返回一个向量组成的矩阵
def get_queries_num(ad):
    a_j = ads.index(ad)
    return graph.transpose()[a_j]


def get_ads(query):
    series = get_ads_num(query).tolist()[0]  # 将其变成向量
    return [ads[x] for x in range(len(series)) if series[x] > 0]


def query_simrank(q1, q2, C):
    if q1 == q2:
        return 1
    # 对应公式里面的C/I(crf.md)I(b)
    prefix = C / (get_ads_num(q1).sum() * get_ads_num(q2).sum())
    postfix = 0
    # 求公式里面的两个求和项
    for ad_i in get_ads(q1):
        for ad_j in get_ads(q2):
            i = ads.index(ad_i)
            j = ads.index(ad_j)
            postfix += ad_sim[i, j]
    return prefix * postfix


def get_queries(ad):
    series = get_queries_num(ad).tolist()[0]  # 将其变成向量
    return [queries[x] for x in range(len(series)) if series[x] > 0]


def ad_simrank(a1, a2, C):
    if a1 == a2:
        return 1
    # 对应公式里面的C/I(crf.md)I(b)
    prefix = C / (get_queries_num(a1).sum() * get_queries_num(a2).sum())
    postfix = 0
    # 求公式里面的两个求和项
    for query_i in get_queries(a1):
        for query_j in get_queries(a2):
            i = queries.index(query_i)
            j = queries.index(query_j)
            postfix += query_sim[i, j]
    return prefix * postfix


def simrank(C=0.8, times=3):
    global query_sim, ad_sim

    for _ in range(times):
        # queries simrank
        new_query_sim = matrix(numpy.identity(len(queries)))
        for qi in queries:
            for qj in queries:
                i = queries.index(qi)
                j = queries.index(qj)
                new_query_sim[i, j] = query_simrank(qi, qj, C)

        # ads simrank
        new_ad_sim = matrix(numpy.identity(len(ads)))
        for ai in ads:
            for aj in ads:
                i = ads.index(ai)
                j = ads.index(aj)
                new_ad_sim[i, j] = ad_simrank(ai, aj, C)

        query_sim = new_query_sim
        ad_sim = new_ad_sim


if __name__ == '__main__':
    simrank()
    print queries
    print query_sim

    print ads
    print ad_sim
