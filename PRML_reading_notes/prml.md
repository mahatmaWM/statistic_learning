
---
## 第2章 概率分布 第3、4章 回归与分类的线性模型 第6、7章 核方法与稀疏核方法 第14章 组合模型的笔记
有较多的公式推导不好书写，所以笔记见纸质本子。

---
## 第5章 神经网络
本章的笔记归纳到深度学习里面。

---
## 第8 9 10 11 12章 图模型、EM、变分推断、采样、LDA知识的学习笔记
第8章
EM算法E步求出隐藏变量的后验概率，M步最大化样本X似然函数的ELOB。

第11章
MCMC采样，pyMC库。

第12章
讲连续的隐藏变量的分析，涉及的例子主要是PCA、概率PCA、贝叶斯PCA等知识。
从两个角度来看PCA，方差最大化或者误差最小化的角度都可以推导出PCA的分解公式，然后讨论了概率PCA的优点以及如何利用EM来求解概率PCA的最大似然估计，
但是前面两种方法都需要人工指定最优的维度K这个数字，最后讨论了贝叶斯PCA的知识，其好处是自动确定合适维度K值，解法是利用变分推导来求解贝叶斯PCA。

LDA的两种参数推导方式变分推断和gibbs采样。

变分推断和采样作为近似推理的两大重要手段，基本上是各有优劣的：采样与变分都是对原分布的近似，只不过采样是以真实数据为基础来近似目标分布，因此更精确，而且采样过程相对简单，易于操作。
变分过程是用一些已知的简单的分布q来近似后验分布p，其推导过程相对复杂，并且这些简单的分布到底能多大程度生近似目标分布呢？
我们不知道，只是优化对应分布之间的KL散度得到最终的结果，容易造成结果的不精确，但是速度比采样要快，毕竟一次期望的计算就节省了很多采样步骤。

Gibbs采样实现参考原始论文 Parameter estimation for text analysis http://www.arbylon.net/publications/text-est.pdf 
变分EM推导见 http://blog.csdn.net/happyer88/article/details/45936107的推导或者原始论文

其余的博文：

    1、[LDA工程实践实现正确性验证 1、2](http://www.flickering.cn/nlp/2014/07/lda%E5%B7%A5%E7%A8%8B%E5%AE%9E%E8%B7%B5%E4%B9%8B%E7%AE%97%E6%B3%95%E7%AF%87-1%E7%AE%97%E6%B3%95%E5%AE%9E%E7%8E%B0%E6%AD%A3%E7%A1%AE%E6%80%A7%E9%AA%8C%E8%AF%81/) 
    这篇文章提到了LDA模型训练过程中，随着迭代的进行，模型的Perplexity曲线会逐渐收敛。
    因此，我们通常会根据训练过程中模型的Perplexity曲线是否收敛来判定模型是否收敛。
    Perplexity曲线收敛性也从侧面可以证明算法实现的正确性，perplexity越小越好。
    另外也有用coherence的方法来评价模型的好坏，coherence是评价每个topic下前面的词语越集中越好，所以coherence值越大越好，对人也更可理解。    
    2、分布式的实现 [Peacock LDA分布式实现](http://forum.ai100.com.cn/blog/thread/ml-2015-03-03-3816245109043572/)
    3、这篇文章普通em与变分推断，采样之间的关系https://zhuanlan.zhihu.com/p/21741426

lda的使用场景：
场景1：文档分类，利用doc-topic矩阵的信息在主题空间进行。
    2

使用的一些例子：
CoherenceModel可以用来判断模型的好坏。
http://gibbslda.sourceforge.net/ 介绍了lda如何使用。
论文中建议alpha=50/K，beta=0.01。
PLSI和LDA的主要区别是，PLSI在document-topic distribution上，没有加任何prior，而LDA假设这个distribution服从一个sparse-inducing的Dirichlet prior. 实际效果就是，PLSI可能学出一个dense的document-topic distribution，即一个文档里，每个topic的概率都有一些，而LDA的document-topic distribution是稀疏的，即大部分topic的概率接近0，少部分topic的概率比较大。这个Dirichlet prior有个参数alpha可以调节稀疏程度，越小越稀疏，也就是每个doc所包含的topic倾向比较集中少数几个。
见dir分布性质的动画https://zh.wikipedia.org/wiki/%E7%8B%84%E5%88%A9%E5%85%8B%E9%9B%B7%E5%88%86%E5%B8%83#/media/File:LogDirichletDensity-alpha_0.3_to_alpha_2.0.gif

问题：如何选择合适的主题K个数？？
方法1、根据数据自动决定合适的主题个数，这类处理方法叫非参数主题模型(Non-parametric Topic Model)，比如HDP利用dirichlet process的性质。
方法2、开始不要设置太大而逐步增大K值，多次试验，看主题之间的相似性越小越好，perplexity越小越好，一般选log(N)量级。
方法3、如果lda仅是一个任务的其中一部分，那么根据总体任务指标来选择合适的K值，比如分类任务中，主题之间相互独立或者存在overlap都可以，只要最后的分类指标好。
DP process徐亦达教授有推导的教学视频，自己也做了笔记。
1. Dirichlet过程的价值：
    非参数方法，无需事先预设cluster的数量，可推广到可数无穷个mixtures的情形；Bayesian方法，比传统的非参数统计更优美。Dirichlet分布作为多项分布的共轭先验，可以绕过推断过程中涉及的一些复杂的积分运算，使得构造有效的推断算法成为可能。
2. Dirichlet分布：
    它是关于多项分布的分布。从Dirichlet分布Dir(alpha, K)中每次抽样，得到的都是一个K维随机向量，且是一个离散分布。alpha是concentration parameter，控制Dirichlet分布的形状，或者说是控制不同多项分布的概率密度。
