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
import elosynthetic as e1
import panda as p
from sklearn.metrics import mean_squared_error
playerRatingTrue,minutesPlayedTrue=s.generateTrueStrength()
#time.sleep(20)
K1=[1,5,10,20,100,200,500,750,1000,1200]
K2=[1,1.5,2,5,10,20,50,100,200,500]
N=10
MSE1=np.zeros((N,100))
MSE2=np.zeros((N,100))
s.statsGenerate(playerRatingTrue,minutesPlayedTrue,1000)
playerRating,minutesPlayedEstimate,MSE=p.estimate(100,2500,minutesPlayedTrue,playerRatingTrue)
#print("2")
#teamRating2,a2 = e1.estimate1(K2[i])
#print("3")
#teamRatingTrue=e.playerToTeamRating(playerRatingTrue,minutesPlayedTrue,minutesPlayedTrue)
#print("4")
#teamRating1 = e.playerToTeamRating1(playerRating, minutesPlayedEstimate, minutesPlayedTrue)
plt.plot(MSE)
plt.xlabel("Number of matches passed")
plt.ylabel("Mean Square Error")
plt.title("System parameters: gamma value=100 and eta value=2500")
plt.show()