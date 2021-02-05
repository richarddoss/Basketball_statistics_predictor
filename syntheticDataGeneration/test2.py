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
playerRatingTrue,minutesPlayedTrue=s.generateTrueStrength()
teamRatingTrue=e.playerToTeamRating(playerRatingTrue,minutesPlayedTrue,minutesPlayedTrue)
time.sleep(20)
K=[20,100,200,500,750,1000]
MSE=np.zeros(6)
s.statsGenerate(playerRatingTrue, minutesPlayedTrue, 1000)
teamRating=e1.estimate1(K[0])
teamRatingTrue=e.playerToTeamRating(playerRatingTrue,minutesPlayedTrue,minutesPlayedTrue)
MSE=e.MeanSquareError(teamRating,teamRatingTrue)
print("MSE",MSE)
'''
#playerRating,TrueStrength=e.estimate(15)
for j in range(10):
    print("Iteration",j)
    s.statsGenerate(playerRatingTrue,minutesPlayedTrue,1000)
    for i in range(6):
        playerRating,minutesPlayedEstimate=e.estimate(K[i])
        teamRatingTrue=e.playerToTeamRating(playerRatingTrue,minutesPlayedTrue,minutesPlayedTrue)
        teamRating = e.playerToTeamRating1(playerRating, minutesPlayedEstimate, minutesPlayedTrue)
        MSE[i]=e.MeanSquareError(teamRating,teamRatingTrue)
        print("K value",K[i],"MSE",MSE[i])
MSEfinal=np.zeros(6)
csv_file1 = open('MSEvalues.csv', 'w')
writer1=csv.writer(csv_file1)
writer1.writerow(["k value","Mean Square Error"])
for i in range(6):
    MSEfinal[i]=np.mean(MSE[i])
    writer1.writerow([K[i],MSEfinal[i]])
csv_file1.close()
plt.plot(K,MSEfinal)
plt.xlabel("K value")
plt.ylabel("Mean square error")
plt.title("Performance metric for the proposed algorithm")
plt.show()
'''