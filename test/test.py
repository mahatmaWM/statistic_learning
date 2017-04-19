from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# We generate some random variates from crf.md non-normal distribution and make crf.md
# probability plot for it, to show it is non-normal in the tails:

fig = plt.figure()
ax1 = fig.add_subplot(211)
x = stats.loggamma.rvs(5, size=5000) + 5
plt.hist(x, bins=50)

ax2 = fig.add_subplot(212)
xt, _ = stats.boxcox(x)
plt.hist(xt, bins=50)

plt.show()
