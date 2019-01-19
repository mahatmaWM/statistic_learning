##word2vec模型
只有一个隐藏层的三层网络，从隐藏层到输出层之间每个样本的计算量都很大，针对这一步提出了一些优化算法，
比如hierarchical softmax和negative sampling，从词典V里面选出k个词语作为正负样本（主要是负样本，因为正样本从数据里面就知道的），
利用二分类的交叉熵来构建loss function，TensorFlow里面两个都实现了。
见[这里的分析](http://www.jianshu.com/p/fab82fa53e16)（Tensorflow 的NCE-Loss的实现）

介绍神经网络与词向量Softmax与Sampling非常好的一篇文章：
中文
http://geek.csdn.net/news/detail/111466
http://geek.csdn.net/news/detail/135736

英文版见：
http://sebastianruder.com/word-embeddings-1/index.html#classicneurallanguagemodel
http://sebastianruder.com/word-embeddings-softmax/index.html#hierarchicalsoftmax
http://sebastianruder.com/secret-word2vec/index.html


word2vec算法细节参考 http://suanfazu.com/t/word2vec-zhong-de-shu-xue-yuan-li-xiang-jie-duo-tu-wifixia-yue-du/178
python实现 https://github.com/mahatmaWM/word2vecpy
word2vec官方实现https://code.google.com/archive/p/word2vec/
word2vec如何评价其效果https://www.zhihu.com/question/37489735
一些可以改进的地方http://licstar.net/archives/620

神经网络语言模型的发展历程（word2vec只是其中一种）
hierarchical softmax的理解https://www.quora.com/What-is-hierarchical-softmax
http://ju.outofmemory.cn/entry/78069

我理解的hierarchical softmax是word2vec里的，如果已知context去求word的概率p直接用softmax的话，需要计算所有词与context的内积，运算量是很大的。
反之，如果构建一个huffman tree，每次进行一次二分，那么求p的话只需要沿着路径从根节点到指向这个词word的叶子节点，把一路上的概率相乘即可，
运算量上小了许多，所以我感觉只是一种减少运算量的方法。
我个人觉得HS除了解决计算的问题，在选择负样本上也隐含了要选择和正样本热门程度差不多的负样本的思想。

这篇文章把神经网络语言模型的发展历程都梳理了一遍，极为推荐
http://www.flickering.cn/nlp/2015/03/%E6%88%91%E4%BB%AC%E6%98%AF%E8%BF%99%E6%A0%B7%E7%90%86%E8%A7%A3%E8%AF%AD%E8%A8%80%E7%9A%84-3%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/
高效word特征求取http://blog.csdn.net/abcjennifer/article/details/46397829，这篇文章对几种模型复杂度的讲解。

[Word2Vec在Tensorflow上的版本以及与Gensim之间的运行对比] http://www.cnblogs.com/edwardbi/p/5511785.html
[Word2vec Tutorial] https://rare-technologies.com/word2vec-tutorial/
