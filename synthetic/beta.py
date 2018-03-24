import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt
a=3
b=3
dist = beta(3, 4)
x = np.linspace(0, 1, 1002)[1:-1]
plt.plot(x, dist.pdf(x))
plt.show()