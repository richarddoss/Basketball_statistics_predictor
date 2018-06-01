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
import pickle
playerRatingTrue,minutesPlayedTrue=s.generateTrueStrength()
#time.sleep(20)
K1=[0,1,5,10,20,100,200,500,750,1000,1200]
K2=[0,1,2,5,10,20,50]
N=7
MSE1=np.zeros((N,100))
MSE2=np.zeros((N,100))
for j in range(100):
    print("Iteration",j)
    s.statsGenerate(playerRatingTrue,minutesPlayedTrue,1000)
    for i in range(N):
        teamRating2,a2 = e1.estimate1(K2[i])
        #print("2")
        teamRatingTrue=e.playerToTeamRating(playerRatingTrue,minutesPlayedTrue,minutesPlayedTrue)
        x2=e.dictToInt(teamRatingTrue)
        x1 = e.dictToInt(teamRating2)
        #print("5")
        MSE2[i][j] = mean_squared_error(x1, x2)
MSE2final=np.zeros(N)
csv_file2 = open('MSEvalues.csv', 'w')
writer2=csv.writer(csv_file2)
writer2.writerow(["k value","Mean Square Error"])
for i in range(N):
    MSE2final[i] = np.mean(MSE2[i])
    writer2.writerow([K2[i], MSE2final[i]])
csv_file2.close()
print(MSE2final)
plt.plot(K2,MSE2final,label='Elo algo')
plt.xlabel("K value")
plt.ylabel("Mean square error")
plt.title("synthetic data(1000 iterations)")
plt.legend()
plt.show()