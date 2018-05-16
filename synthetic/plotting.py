from collections import defaultdict
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
import pickle
'''
gamma=[25, 50, 75,  100, 250, 500]
eta=[1000,2500,5000, 10000]
f = open("MSE",'rb')
MSE=pickle.load(f)
print(np.shape(MSE))
MSE1=np.zeros(24)
for i in range(24):
    MSE1[i]=np.mean(MSE[i][:])
print(MSE1)
MSE1=np.reshape(np.transpose(MSE1),[6,4])
MSE1=np.transpose(MSE1)
print(np.shape(gamma),np.shape(eta),np.shape(MSE1))
X,Y=np.meshgrid(gamma,eta)
print(np.shape(X),np.shape(Y))
print(X)
print(Y)
print(MSE1)
#ax = plt.axes(projection='3d')
#ax.scatter(X, Y, MSE1, cmap='green', linewidth=0.5);
#ax.plot3D(K1, N1, P, 'gray')
#cp=ax.plot_surface(X, Y, MSE1, rstride=1, cstride=1,cmap='viridis', edgecolor='none')
#plt.colorbar(cp)
#ax.set_xlabel('gamma value')
#ax.set_ylabel('eta value')
#ax.set_zlabel('Number of correct predictions')
#plt.show()
'''
MSE1000=[2684.47,2426.67,2335.38,2332.27,2966.21,5865.55]
MSE2500=[2522.53,2215.44,2072.15,2030.35,2721.70,5310.43]
MSE5000=[2544.45,2312.99,2185.66,2146.72,2923.67,5703.31]
MSE10000=[2600.68,2494.92,2417.65,2400.39,3279.50,6278.10]
gamma=[25,50,75,100,250,500]
plt.plot(gamma, MSE1000, label='eta value=1000')
plt.plot(gamma, MSE2500, label='eta value=2500')
plt.plot(gamma, MSE5000, label='eta value=5000')
plt.plot(gamma, MSE10000, label='eta value=10000')
plt.xlabel("gamma values")
plt.ylabel("Mean Square Error")
plt.title("Mean Square value curves for various values of eta")
plt.legend()
plt.show()
