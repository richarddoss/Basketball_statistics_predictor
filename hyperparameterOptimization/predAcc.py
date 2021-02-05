from collections import defaultdict
import collections
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
import function as f
import sklearn.metrics as m
MSE2500=[337, 328, 312, 302]
MSE10000=[372, 390, 387, 354]
MSE25000=[382,391,388, 382]
MSE100000=[384,387,388, 386]
gamma=[10,250,500,1000]
plt.plot(gamma, MSE2500, label='eta value=2500')
#plt.plot(gamma, MSE5000, label='eta value=5000')
plt.plot(gamma, MSE10000, label='eta value=10000')
plt.plot(gamma, MSE25000, label='eta value=25000')
plt.plot(gamma, MSE100000, label='eta value=100000')
plt.xlabel("gamma values")
plt.ylabel("Mean Square Error")
plt.title("Number of correct predictions curves for various values of eta")
plt.legend()
plt.show()
'''
K=[1,2,5,10,20,30,50,100,200,500]
P=[362,366,387,385,387,391,389,376,365,353]
plt.plot(K,P,label="Elo algorithm")
plt.xlabel("K value")
plt.ylabel("Number of Correct Predictions")
plt.title("Elo algorithm (Total games=615)")
plt.legend()
plt.show()
'''