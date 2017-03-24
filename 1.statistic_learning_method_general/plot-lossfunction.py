# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10, 10, 10000)
y = np.exp(-np.abs(x))
z = 1 / (1 + np.abs(x))

plt.figure(figsize=(8, 4))
plt.plot(x, y, label="$exp(-x)$", color="red", linewidth=2)
plt.plot(x, z, "b--", label="$1/(1+abs(x))$")
plt.xlabel("x")
plt.ylabel("y")
plt.title("PyPlot First Example")
plt.ylim(0, 1.2)
plt.legend()
plt.show()
