本章代码是阅读李航老师的教材写的。有信息增益ID3以及信息增益率C45，以及CART树中的gini系数以及平方误差最小的实现例子。

Tips on practical use：特别高维特征（相当于样本个数相对特征个数就变小了）容易overfitting，所以用之前降维是蛮重要的。
另外max-depth、min-samples*等参数，对于unbalance的数据也有一些参数来控制，对于稀疏数据也有处理。这些处理也可以看做是在对模型进行regularization。
ID3, C4.5, C5.0 and CART 这些都是构建单棵树的时候采用的方法。
其中ID3用信息增益，而C4.5做了修正用信息增益比，这样可以解决信息增益偏向选择取值较多的特征的问题，C5.0是在4.5基础上做了优化，可以处理大数据，是4.5的商业化版本。
CART对于回归树用平方误差最小化准则，对于分类树用基尼指数最小化准则。
再多说一点，首先DT树都是二叉树。ID3具体在操作的时候，如果某一个feature被选中作为分裂特征，而这个feature下面可能有多个取值，则以数目最多的那个作为标记。C4.5也是一样的操作。而对于CART的gini系数，则要针对每个feature的每一个取值做gini计算，求出最优的feature以及此feature中的最优切割。
classification criteria和regression criteria：gini、cross-entropy、misclassification以及MSE。