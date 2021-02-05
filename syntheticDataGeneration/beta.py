import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt
a=3
b=3
dist = beta(11.02,11.02)
x = np.linspace(0, 1, 1002)[1:-1]
x1=x*48
plt.plot(x1, dist.pdf(x))
plt.xlabel("Time spent on the court")
plt.ylabel("Probability density")
plt.title("Distribution of the time played by professional basketball players")
plt.show()