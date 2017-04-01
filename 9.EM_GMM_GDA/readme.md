高斯判别模型和高斯混合模型，前者用于分类，后者用于聚类，
原理一样，只是后者对目标分布没有先验知识，所以两者求解的过程不一样。
这个页面推导GDA公式和笔记一样 http://www.cnblogs.com/sumai/p/5258081.html 这个页面推导GMM EM实现和笔记一样，
也可以见李航老师教材9章163页
http://blog.csdn.net/chasdmeng/article/details/38709063 这是一个最简单的实现，没有考虑sigma和系数alpha，只迭代mu


EM的算法思想见[NG的课件](http://cs229.stanford.edu/notes/cs229-notes8.pdf)还有[yida.xu老师的课件](http://www-staff.it.uts.edu.au/~ydxu/ml_course/)，两者讲解的方式有点差别，本质一样，NG对收敛迭代性的证明很巧。
从NG的课件中可见：
  E步：已知样本X以及猜测参数theta，求隐藏变量z的分布，将其带入似然函数L的lowerbound。
  M步：求使似然函数L的lowerbound值最大的参数newtheta。
循环以上步骤知道收敛。
