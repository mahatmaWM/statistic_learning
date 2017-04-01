本章代码是阅读李航老师的教材写的。

Tips on practical use：特别高维特征的数据，样本个数相对特征个数变得很小，容易over fitting，所以对数据做降维预处理是必要的。
另外max-depth、min-samples-等参数，对于unbalance的数据也有一些参数来控制，对于稀疏数据也有处理。这些处理也可以看做是在对模型进行regularization。

ID3, C4.5, C5.0 and CART：
>* ID3用信息增益，而C4.5做了修正用信息增益比，以解决信息增益偏向选择 分类取值较多的特征的问题，C5.0是在4.5基础上做了优化，可以处理大数据。
>* CART对于回归树用平方误差最小化准则，对于分类树用基尼指数最小化准则 作为树分裂的准则，并用valid数据来选择最优树。
>* 首先DT树都是二叉树。ID3具体在操作的时候，如果某一个feature被选中作为分裂特征，而这个feature下面可能有多个取值，则以数目最多的那个作为标记。C4.5也是一样的操作。而对于CART的gini系数，则要针对每个feature的每一个取值做gini计算，求出最优的feature以及此feature中的最优切割。
>* classification criteria和regression criteria：gini、cross-entropy、misclassification以及MSE。
