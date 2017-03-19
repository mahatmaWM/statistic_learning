# coding=utf-8
"""
这个例子展示了scikit里面如何做特征选择
"""
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier

# 四个维度
iris = load_iris()
# print(iris.data)

# 用GBDT作为基模型进行特征选择，fit出模型，在transform数据
print(SelectFromModel(GradientBoostingClassifier().fit_transform(iris.data, iris.target)))

# 带L1惩罚项的逻辑回归作为基模型的特征选择，展现不同惩罚力度对参数的影响
print(SelectFromModel(LogisticRegression(penalty="l1", C=0.1).fit_transform(iris.data, iris.target)))
print(SelectFromModel(LogisticRegression(penalty="l1", C=0.01).fit_transform(iris.data, iris.target)))

print(SelectFromModel(LogisticRegression(penalty="l2", C=1).fit_transform(iris.data, iris.target)))
print(SelectFromModel(LogisticRegression(penalty="l2", C=0.1).fit_transform(iris.data, iris.target)))
