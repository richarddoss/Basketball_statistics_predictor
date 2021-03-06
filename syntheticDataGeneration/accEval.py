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
#time.sleep(20)
K1=[1,5,10,20,100,200,500,750,1000,1200]
K2=[1,1.5,2,5,10,20,50,100,200,500]
N=10
MSE1=np.zeros((N,10))
acc1=np.zeros((N,10))
acc2=np.zeros((N,10))
for j in range(10):
    print("Iteration",j)
    s.statsGenerate(playerRatingTrue,minutesPlayedTrue,1000)
    for i in range(N):
        playerRating,minutesPlayedEstimate,a1=e.estimate(K1[i])
        teamRating2,a2 = e1.estimate1(K2[i])
        #teamRatingTrue=e.playerToTeamRating(playerRatingTrue,minutesPlayedTrue,minutesPlayedTrue)
        #teamRating1 = e.playerToTeamRating1(playerRating, minutesPlayedEstimate, minutesPlayedTrue)
        #MSE1[i][j]=e.MeanSquareError(teamRating1,teamRatingTrue)
        #MSE2[i][j] = e.MeanSquareError(teamRating2, teamRatingTrue)
        acc1[i][j]=a1
        acc2[i][j]=a2
        print("K1 value",K1[i],"MSE",acc1[i][j])
        print("K2 value", K2[i], "MSE", acc2[i][j])

MSE1final=np.zeros(N)
MSE2final=np.zeros(N)
'''
csv_file1 = open('MSEvaluesThesis.csv', 'w')
csv_file2 = open('MSEvalues.csv', 'w')
writer1=csv.writer(csv_file1)
writer2=csv.writer(csv_file2)
writer1.writerow(["k value","Mean Square Error"])
writer2.writerow(["k value","Mean Square Error"])
'''
for i in range(N):
    MSE1final[i]=np.mean(acc1[i])
    MSE2final[i] = np.mean(acc2[i])
    #writer1.writerow([K1[i],MSE1final[i]])
    #writer2.writerow([K2[i], MSE2final[i]])
#csv_file1.close()
plt.plot(K1,MSE1final,label='proposed algo')
plt.plot(K2,MSE2final,label='conventional algo')
plt.xlabel("K value")
plt.ylabel("Mean square error")
plt.title("Prediction accuracy of two algorithm")
plt.legend()
plt.show()