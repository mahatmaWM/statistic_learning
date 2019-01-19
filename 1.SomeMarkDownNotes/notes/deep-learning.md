##CNN的学习记录

http://blog.csdn.net/v_july_v/article/details/51812459 
这篇文章对cnn的convolution层、pooling层等介绍很清晰，如何估算每个convolution层的输入输出个数就变得很直观，这个思路和TensorFlow里面的代码实现一一对应，最简单的例子实现见莫烦的例子：


用标准CNN需要满足的三个特性，卷积层的意思。
1, some patterns are much smaller than the whole image.
2, same patterns appear in different areas.
3, subsampling, get subpart that active the function.


##RNN的学习记录
非常好的rnn介绍网页 http://karpathy.github.io/2015/05/21/rnn-effectiveness/
http://blog.csdn.net/Dark_Scope/article/details/47056361

运行PTB例子
Penn TreeBank（PTB）数据集被用在很多语言建模（Language Modeling）的论文中，
包括”Empirical Evaluation and Combination of Advanced Language Modeling Techniques” 
和 “Recurrent Neural Network Regularization”。该数据集的训练集有929k个单词，验证集有73K个单词，测试集有82k个单词。 
在它的词汇表刚好有10k个单词。

PTB例子是为了展示如何用递归神经网络（Recurrent Neural Network）来进行语言建模的。

给一句话 “I am from Imperial College London”, 这个模型可以从中学习出如何从“from Imperial College”来预测出“Imperial College London”。
也就是说，它根据之前输入的单词序列来预测出下一步输出的单词序列，在刚才的例子中 num_steps (序列长度，sequence length) 为 3。


##梯度消失或者梯度爆炸
w、b参数初始化太小<1，容易造成梯度消失
w、b参数初始化太大，容易造成梯度爆炸

后面层的梯度是前面层的梯度累积的乘积，所以神经网络非常不稳定，要么越来越小，要么越来越大。在rnn尤其明显，所以有lstm来解决这个问题。


##Batch Normalization
在机器学习中数据标准化有很多好处，bn是借鉴了这一思路并在深度学习中使用。
它标准化每一层输入数据将其变换到激励函数最鲜活的区间，尽量避开饱和区间，从而使各层的激励函数都能很好的发挥作用。
饱和区间的副作用很大，对数据分布的影响很大。
bn还有两个平移和缩放的因子是由模型训练得到的，经过平移和缩放处理之后，标准化的时候改变的特征分布就能够被重新构造出来。
以下两篇博文解释的很好。
http://blog.csdn.net/hjimce/article/details/50866313
http://www.jianshu.com/p/0312e04e4e83


##教材<深度学习>一书的读书笔记
第一部分 2 3 4 5 章是基础知识

第二部分 6 7 8 9 10 11 12章是实践工作

第三部分 

##聊一聊深度学习的activation function
https://zhuanlan.zhihu.com/p/25110450