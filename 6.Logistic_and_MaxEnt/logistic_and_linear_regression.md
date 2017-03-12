<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    extensions: ["tex2jax.js"],
    jax: ["input/TeX", "output/HTML-CSS"],
    tex2jax: {
      inlineMath: [ ['$','$'], ["\\(","\\)"] ],
      displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
      processEscapes: true
    },
    "HTML-CSS": { availableFonts: ["TeX"] }
  });
</script>
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

# 逻辑回归 
假设y变量服从伯努力分布，则有$P(y=1|x;\theta)=h_\theta(x)$，$P(y=0|x;\theta)=1-h_\theta(x)$，统一为以下形式： 
$$P(y|x;\theta)=(h_\theta(x))^y(1-h_\theta(x))^{(1-y)}$$ 
假设一个函数
$$h_\theta(x)=g(\theta^Tx)=\frac{1}{1+e^{-\theta^Tx}}$$ 
$g(z)=\frac{1}{1+e^{-z}}$这个函数叫sigmod函数，它有特性$\frac{\partial g(z)}{\partial z}=g(z)(1-g(z))$，推导时会用到。
用最大似然估计有： 
$$L(\theta)=p(\vec{y}|X;\theta)$$ 
$$L(\theta)=\prod_{i=1}^{m}(h_\theta(x^{(i)}))^{y^{(i)}}(1-h_\theta(x^{(i)}))^{(1-y^{(i)})}$$
取对数并求导有：
$$\frac{\partial }{\partial \theta_j}l(\theta)=(y\frac{1}{g(\theta^Tx)}-(1-y)\frac{1}{1-g(\theta^Tx)}))\frac{\partial }{\partial \theta_j}g(\theta^Tx)$$ 
接下来的问题就相当熟悉了，我们可以使用梯度下降，最大似然函数。 
$$\frac{\partial }{\partial \theta_j}l(\theta)=(y\frac{1}{g(\theta^Tx)}-(1-y)\frac{1}{1-g(\theta^Tx)}))\frac{\partial }{\partial \theta_j}g(\theta^Tx)$$ 
$$\frac{\partial }{\partial \theta_j}l(\theta)=(y\frac{1}{g(\theta^Tx)}-(1-y)\frac{1}{1-g(\theta^Tx)}))g(\theta^Tx)(1-g(\theta^Tx))\frac{\partial }{\partial \theta_j}\theta^Tx$$ 
$$\frac{\partial }{\partial \theta_j}l(\theta)=(y(1-g(\theta^Tx))-(1-y)g(\theta^Tx))x_j$$ 
$$\frac{\partial }{\partial \theta_j}l(\theta)=(y-h_\theta(x))x_j$$ 
最后的迭代公式为： 
$$\theta_{j+1}\doteq \theta_{j}+\alpha \sum_{i=1}^{m}\left (y^{(i)}-h_{\theta}(x^{(i)}) \right )x_{j}^{(i)}$$ 

# 线性回归 
下式是最小二乘的损失函数，但是没有告知如何得到 
$$J(\theta )= \frac{1}{2}\sum_{i=1}^{m}(h_\theta (x)^{(i)}-y{(i)})^{2}$$ 
以下根据概率模型推导出这个损失函数，下面是一种概率解释：让我们回到一开始的式子来看一看，
一开始我们定义线性回归方程$y^{(i)}=\theta^{T}x^{(i)}+\varepsilon^{(i)}$， 
其中是我们的误差项$\varepsilon^{(i)}$，假设它是独立同分布(IID)的高斯分布，
即$\varepsilon^{(i)}\sim N(0,\sigma ^2)$（假设它为高斯分布，我们主要用了概率统计里的一个很重要的定理：中心极限定理），
那么我们可以得到： 
$$p(\varepsilon ^{(i)})=\frac{1}{\sqrt{2\pi }\sigma }exp(-\frac{(\varepsilon ^{(i)})^2}{2\sigma ^2})$$ 
将线性回归方程代入到我们得到： 
$$p(y^{(i)}|x^{(i)};\theta)=\frac{1}{\sqrt{2\pi}\sigma } exp(-\frac{(y^{(i)}-\theta ^Tx^{(i)})^2}{2\sigma ^2})$$ 
从而我们可以得到我们的似然（likelihood）函数 
$$L(\theta )=L(\theta ;X,\vec{y})=p(\vec{y}|X;\theta )$$ 
$$L(\theta )=\prod_{i=1}^{m}p(y^{(i)}|x^{(i)};\theta )$$ 
$$L(\theta )=\prod_{i=1}^{m}\frac{1}{\sqrt{2\pi}\sigma }exp(-\frac{(y^{(i)}-\theta^Tx^{(i)})^2}{2\sigma ^2})$$ 
对此似然函数进行极大似然估计(MLE)，求对数再进行极大似然估计，函数会变得比较简单,所以log likelihood l(Θ): 
$$l(\theta )=logL(\theta)=\sum_{i=1}^{m}log\frac{1}{\sqrt{2\pi}\sigma }exp(-\frac{(y^{(i)}- \theta^Tx^{(i)})^2}{2\sigma ^2})$$ 
$$l(\theta )=mlog\frac{1}{\sqrt{2\pi}\sigma}-\frac{1}{\sigma^2}\frac{1}{2}\sum_{i=1}^{m}(y^{(i)}-\theta^Tx^{(i)})^2$$ 
$$l(\theta )=c_1-c_2\frac{1}{2}\sum_{i=1}^{m}(y^{(i)}-\theta^Tx^{(i)})^2$$ 
至此，我们最大化似然函数l(Θ)，等价于最小化损失函数J(Θ)，这也说明了在我们的推导中，
最后结果与我们假设的高斯分布的方差σ是没有关系的。 
我们回过头来再考虑一下，我们假设了什么，我们假设误差项服从高斯分布，
这个假设对于线性回归模型来说非常形象，其实我们一开始就假设了这个模型是一个线性模型，
那么很自然的我们会考虑误差一定是离线性函数越近可能性越大，离线性函数越远可能性越小。
所以在机器学习模型中，假设对于我们来说相当重要。
我的感受是：任何的机器学习算法都不能被称为一定是一个好的算法，只有当我们的假设符合数据本身的性质，
我们的机器学习模型才能达到一个好的效果。