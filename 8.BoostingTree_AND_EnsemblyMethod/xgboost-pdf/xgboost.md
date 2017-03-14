[官网介绍](https://xgboost.readthedocs.io/en/latest/model.html)，使用CART树作为基模型。
[使用例子以及参数使用](https://xgboost.readthedocs.io/en/latest/how_to/param_tuning.html)

xgbdt不同于gbdt的地方：
1、使用了损失函数的二阶导数，也考虑了每个子树的复杂度防止过拟合，最后在组合子树的时候也考虑了shrinkage的问题，进一步防止模型过拟合。
2、因为1使得每次子树拟合的目标也与gbdt不一样，这样有二次海森矩阵了；gbdt只有梯度和步长。