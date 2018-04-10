import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt

def logistic(x):
    y = (1 / (1 + pow(10, -(x)/40 )))-0.5
    return (y)

x = np.linspace(-120, 120, 1002)
y=logistic(x)
plt.plot(x, y)
plt.xlabel("x(The difference between the actual score and expected score")
plt.ylabel("F(x)")
plt.title("The function chosen to regulate the update in algorithm")
plt.show()