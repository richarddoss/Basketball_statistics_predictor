from collections import defaultdict
import collections
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
import random
import statGeneration as s
import estimation as e
playerRatingTrue,minutesPlayedTrue=s.generateTrueStrength()
s.statsGenerate(playerRatingTrue,minutesPlayedTrue,1000)
K=[20,100,200,500,750,1000]
MSE=[0,0,0,0,0,0]
playerRating,TrueStrength=e.estimate(15)
'''
for i in range(6):
    playerRating,TrueStrength=e.estimate(K[i])
    MSE[i]=e.MeanSquareError(playerRating,TrueStrength)
plt.plot(MSE)
plt.show()
'''