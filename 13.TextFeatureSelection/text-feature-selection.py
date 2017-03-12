#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_files
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


def pre_compute(doc_terms_x_list, doc_class_y_list):
    # 文档有多少个类别
    class_set = sorted(list(set(doc_class_y_list)))
    class_dict = dict(zip(class_set, range(len(class_set))))
    # 每个term以及term在字典中索引位置
    terms_dict = {}
    for doc_terms in doc_terms_x_list:
        for term in doc_terms:
            terms_dict[term] = 1
    term_set_list = sorted(terms_dict.keys())  # term set排序后，按照索引做出字典
    terms_dict = dict(zip(term_set_list, range(len(term_set_list))))
    # 统计每个类别包含了多少个文档
    class_df_list = [0] * len(class_dict)
    for doc_class in doc_class_y_list:
        class_df_list[class_dict[doc_class]] += 1
    return {'class_dict': class_dict, 'terms_dict': terms_dict, 'class_df_list': class_df_list}


# 遍历每一篇文章,将出现过的term往 term数目*class类别数目 这个矩阵里面填写,出现一次就加1,在同一篇文档里面出现多次的term被认为出现一次
def compute_terms_classes_matrix(doc_terms_x_list, doc_class_y_list, terms_dict, class_dict):
    term_class_df_mat = np.zeros((len(terms_dict), len(class_dict)), np.float32)
    for k in range(len(doc_class_y_list)):
        class_index = class_dict[doc_class_y_list[k]]
        doc_terms = doc_terms_x_list[k]
        for term in set(doc_terms):
            term_index = terms_dict[term]
            term_class_df_mat[term_index][class_index] += 1
    return term_class_df_mat


def feature_selection_mi(class_df_list, terms_set, term_class_df_mat):
    A = term_class_df_mat  # 本来就是特征词Ti属于Cj的个数
    B = np.array([(sum(x) - x).tolist() for x in A])  # 作差就是特征词Ti,不属于Cj的个数
    C = np.tile(class_df_list,
                (A.shape[0], 1)) - A  # 将每个类别包含的文档的数目list往下拉伸与A作差,每个元素代表的意思就是不包含Ti且属于Cj类别的文档数目,np.tile的使用很巧妙
    N = sum(class_df_list)
    class_set_size = len(class_df_list)

    term_score_mat = np.log(
        ((A + 1.0) * N) / ((A + C) * (A + B + class_set_size)))  # 加了一个拉普拉斯平滑因子，防止分子为0的情况，这里也可以看出互信息倾向选低频词
    term_score_max_list = [max(x) for x in term_score_mat]
    term_score_array = np.array(term_score_max_list)
    sorted_term_score_index = term_score_array.argsort()[:: -1]  # argsort 返回的是数组值从小到大的索引值
    term_set_fs = [terms_set[index] for index in sorted_term_score_index]

    return term_set_fs


def feature_selection_ig(class_df_list, term_set, term_class_df_mat):
    A = term_class_df_mat
    B = np.array([(sum(x) - x).tolist() for x in A])
    C = np.tile(class_df_list, (A.shape[0], 1)) - A
    N = sum(class_df_list)
    D = N - A - B - C
    term_df_array = np.sum(A, axis=1)
    class_set_size = len(class_df_list)

    p_t = term_df_array / N
    p_not_t = 1 - p_t
    p_c_t_mat = (A + 1) / (A + B + class_set_size)
    p_c_not_t_mat = (C + 1) / (C + D + class_set_size)
    p_c_t = np.sum(p_c_t_mat * np.log(p_c_t_mat), axis=1)
    p_c_not_t = np.sum(p_c_not_t_mat * np.log(p_c_not_t_mat), axis=1)

    term_score_array = p_t * p_c_t + p_not_t * p_c_not_t
    sorted_term_score_index = term_score_array.argsort()[:: -1]
    term_set_fs = [term_set[index] for index in sorted_term_score_index]

    return term_set_fs


def feature_selection_wllr(class_df_list, term_set, term_class_df_mat):
    A = term_class_df_mat
    B = np.array([(sum(x) - x).tolist() for x in A])
    C_Total = np.tile(class_df_list, (A.shape[0], 1))
    N = sum(class_df_list)
    C_Total_Not = N - C_Total
    term_set_size = len(term_set)

    p_t_c = (A + 1E-6) / (C_Total + 1E-6 * term_set_size)
    p_t_not_c = (B + 1E-6) / (C_Total_Not + 1E-6 * term_set_size)
    term_score_mat = p_t_c * np.log(p_t_c / p_t_not_c)

    term_score_max_list = [max(x) for x in term_score_mat]
    term_score_array = np.array(term_score_max_list)
    sorted_term_score_index = term_score_array.argsort()[:: -1]
    term_set_fs = [term_set[index] for index in sorted_term_score_index]

    return term_set_fs


def feature_selection_wfo(class_df_list, term_set, term_class_df_mat, lamda=0.5):
    A = term_class_df_mat
    B = np.array([(sum(x) - x).tolist() for x in A])
    C_Total = np.tile(class_df_list, (A.shape[0], 1))
    N = sum(class_df_list)
    C_Total_Not = N - C_Total
    term_set_size = len(term_set)

    p_t_c = (A + 1E-6) / (C_Total + 1E-6 * term_set_size)
    p_t_not_c = (B + 1E-6) / (C_Total_Not + 1E-6 * term_set_size)

    # if p_t_c/p_t_not_c > 1:
    term_score_mat = (p_t_c ** lamda) * np.log((p_t_c ** (1 - lamda)) / p_t_not_c)

    TEMP = p_t_c / p_t_not_c
    rows = TEMP.shape[0]
    colums = TEMP.shape[1]
    for i in range(rows):
        for j in range(colums):
            if TEMP[i][j] <= 1:
                term_score_mat[i][j] = 0

    term_score_max_list = [max(x) for x in term_score_mat]
    term_score_array = np.array(term_score_max_list)
    sorted_term_score_index = term_score_array.argsort()[:: -1]
    term_set_fs = [term_set[index] for index in sorted_term_score_index]

    return term_set_fs


def feature_selection(doc_terms_x_list, doc_class_y_list, fs_method):
    pre = pre_compute(doc_terms_x_list, doc_class_y_list)
    class_dict = pre.get('class_dict')
    terms_dict = pre.get('terms_dict')
    class_df_list = pre.get('class_df_list')

    term_class_df_mat = compute_terms_classes_matrix(doc_terms_x_list, doc_class_y_list, terms_dict, class_dict)
    term_set = [term[0] for term in sorted(terms_dict.items(), key=lambda x: x[1])]
    term_set_fs = []

    if fs_method == 'MI':
        term_set_fs = feature_selection_mi(class_df_list, term_set, term_class_df_mat)
    elif fs_method == 'IG':
        term_set_fs = feature_selection_ig(class_df_list, term_set, term_class_df_mat)
    elif fs_method == 'WLLR':
        term_set_fs = feature_selection_wllr(class_df_list, term_set, term_class_df_mat)
    elif fs_method == 'WFO':
        term_set_fs = feature_selection_wfo(class_df_list, term_set, term_class_df_mat)

    return term_set_fs


# 使用scikit的CountVectorizer,将term集合指定为自定义的集合
def text_classifly_twang(dataset_dir_name, fs_method, fs_num):
    print 'Loading dataset, 80% for training, 20% for testing...'
    movie_reviews = load_files(dataset_dir_name)

    # 返回的四个list的含义
    doc_str_list_train, doc_str_list_test, doc_class_list_train, doc_class_list_test = train_test_split(
        movie_reviews.data, movie_reviews.target, test_size=0.3, random_state=10)

    print 'Feature selection...'
    print 'fs method:' + fs_method, ' fs num:' + str(fs_num)
    vectorizer = CountVectorizer(binary=True)

    # 切词并得到term set feature select
    word_tokenizer = vectorizer.build_tokenizer()
    doc_terms_list_train = [word_tokenizer(doc_str) for doc_str in doc_str_list_train]
    term_set_fs = feature_selection(doc_terms_list_train, doc_class_list_train, fs_method)[:fs_num]

    print 'Building VSM model...with'
    term_dict = dict(zip(term_set_fs, range(len(term_set_fs))))

    vectorizer.set_params(vocabulary=term_dict)

    doc_train_vec = vectorizer.fit_transform(doc_str_list_train)
    doc_test_vec = vectorizer.transform(doc_str_list_test)

    clf = MultinomialNB().fit(doc_train_vec, doc_class_list_train)  # 调用MultinomialNB分类器
    doc_test_predicted = clf.predict(doc_test_vec)

    acc = np.mean(doc_test_predicted == doc_class_list_test)
    print 'Accuracy: ', acc

    return acc


if __name__ == '__main__':
    dataset_dir_name = './txt_sentoken/'
    fs_method_list = ['IG', 'MI', 'WLLR', 'WFO']
    # fs_method_list = ['WFO']
    fs_num_list = range(100, 1000, 100)
    acc_dict = {}

    for fs_method in fs_method_list:
        acc_list = []
        for fs_num in fs_num_list:
            acc = text_classifly_twang(dataset_dir_name, fs_method, fs_num)
            acc_list.append(acc)
        acc_dict[fs_method] = acc_list
        print 'fs method:', acc_dict[fs_method]

    for fs_method in fs_method_list:
        plt.plot(fs_num_list, acc_dict[fs_method], '--^', label=fs_method)
        plt.title('feature  selection')
        plt.xlabel('fs num')
        plt.ylabel('accuracy')
        plt.ylim((0.40, 0.86))

    plt.legend(loc='upper left', numpoints=1)
    plt.show()
