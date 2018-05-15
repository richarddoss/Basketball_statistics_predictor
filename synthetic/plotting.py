from collections import defaultdict
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
import pickle
gamma=[100, 250, 500]
eta=[1000,2500,10000]
f = open("MSE",'rb')
MSE=pickle.load(f)
MSE1=np.zeros(9)
for i in range(9):
    MSE1[i]=np.mean(MSE[i][:])
print(MSE1)
MSE1=np.reshape(np.transpose(MSE1),[3,3])
MSE1=np.transpose(MSE1)
print(np.shape(gamma),np.shape(eta),np.shape(MSE1))
X,Y=np.meshgrid(gamma,eta)
print(np.shape(X),np.shape(Y))
print(X)
print(Y)
ax = plt.axes(projection='3d')
ax.scatter(X, Y, MSE1, cmap='green', linewidth=0.5);
#ax.plot3D(K1, N1, P, 'gray')
#cp=ax.plot_surface(X, Y, MSE1, rstride=1, cstride=1,cmap='viridis', edgecolor='none')
#plt.colorbar(cp)
ax.set_xlabel('gamma value')
ax.set_ylabel('eta value')
ax.set_zlabel('Number of correct predictions')
plt.show()