import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt
a=3
b=3
dist = beta(70, 70)
x = np.linspace(0, 1, 1002)[1:-1]
x1=x*600+900
plt.plot(x1, dist.pdf(x))
plt.xlabel("Player's true strength")
plt.ylabel("Probability density")
plt.title("Distribution of the strengths of professional basketball players")
plt.show()