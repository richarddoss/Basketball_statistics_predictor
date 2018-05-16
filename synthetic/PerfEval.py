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
eta1=[1000,2500,500,10000]
gamma1=[50,100,250,500]
gamma=[25,25,25,25,50,50,50,50,75,75,75,75, 100,100,100,100,250,250,250,250,500,500,500,500]
eta=[1000,2500, 5000, 10000,1000,2500,5000, 10000,1000,2500,5000, 10000, 1000,2500,5000, 10000,1000,2500, 5000, 10000,1000,2500, 5000, 10000]
N=24
MSE1=np.zeros((N,100))
MSE2=np.zeros((N,100))
for j in range(100):
    print("Iteration",j)
    s.statsGenerate(playerRatingTrue,minutesPlayedTrue,1000)
    for i in range(N):
        #print("1")
        playerRating,minutesPlayedEstimate=p.estimate(gamma[i],eta[i])
        #print("2")
        #teamRating2,a2 = e1.estimate1(K2[i])
        #print("2")
        teamRatingTrue=e.playerToTeamRating(playerRatingTrue,minutesPlayedTrue,minutesPlayedTrue)
        #print(teamRatingTrue)
        #time.sleep(2)
        #print("4")
        teamRating1 = e.playerToTeamRating1(playerRating, minutesPlayedEstimate, minutesPlayedTrue)
        #print("5")
        #x1=e.dictToInt(teamRating1)
        #print("3")
        x2=e.dictToInt(teamRatingTrue)
        #MSE1[i][j]=mean_squared_error(x1,x2)
        #MSE1[i][j]=e.MeanSquareError(teamRating1,teamRatingTrue)
        #print("6")
        #print("4")
        x1 = e.dictToInt(teamRating1)
        #print("5")
        MSE2[i][j] = mean_squared_error(x1, x2)
        #print("6")
        #MSE2[i][j] = e.MeanSquareError(teamRating2, teamRatingTrue)
        #print("7")
        #print("K1 value",K1[i],"MSE",MSE1[i][j])
        #print("gamma value", gamma[i],"eta value", eta[i], "MSE", MSE2[i][j])
        #time.sleep(2)

pickle_out = open("gamma","wb")
pickle.dump(gamma1,pickle_out)
pickle_out.close()
pickle_out = open("eta","wb")
pickle.dump(eta1,pickle_out)
pickle_out.close()
#for i in range(N):
#    MSE2final[i] = np.mean(MSE2[i])
pickle_out = open("MSE","wb")
pickle.dump(MSE2,pickle_out)
pickle_out.close()
'''
#MSE1final=np.zeros(N)
MSE2final=np.zeros(N)
csv_file1 = open('MSEvaluesThesis.csv', 'w')
#csv_file2 = open('MSEvalues.csv', 'w')
writer1=csv.writer(csv_file1)
#writer2=csv.writer(csv_file2)
#writer1.writerow(["k value","Mean Square Error"])
writer1.writerow(["k value","Mean Square Error"])
for i in range(N):
    #MSE1final[i]=np.mean(MSE1[i])
    MSE2final[i] = np.mean(MSE2[i])
    #writer1.writerow([K1[i],MSE1final[i]])
    writer2.writerow([K2[i], MSE2final[i]])
#csv_file1.close()
csv_file2.close()
#plt.plot(K1,MSE1final,label='proposed algo')
#plt.plot(K2,MSE2final,label='Elo algo')
X,Y=np.meshgrid(gamma,eta)
print(np.shape(X),np.shape(Y))
print(X)
print(Y)
ax = plt.axes()
#ax.plot3D(K1, N1, P, 'gray')
cp=ax.contour(X, Y, P)
plt.colorbar(cp)
ax.set_xlabel('gamma value')
ax.set_ylabel('eta value')
#ax.set_zlabel('Number of correct predictions')
#plt.show()
#plt.xlabel("K value")
#plt.ylabel("Mean square error")
plt.title("synthetic data")
plt.legend()
plt.show()
'''