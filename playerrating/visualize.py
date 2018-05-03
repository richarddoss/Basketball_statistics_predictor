from collections import defaultdict
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
import function as f
from mpl_toolkits import mplot3d
import pickle
f = open("K1",'rb')
K1=pickle.load(f)
f = open("N1",'rb')
N1=pickle.load(f)
f = open("P",'rb')
P=pickle.load(f)
print(np.shape(K1),np.shape(N1),np.shape(P))
X,Y=np.meshgrid(N1,K1)
print(np.shape(X),np.shape(Y))
print(X,Y)
ax = plt.axes()
#ax.plot3D(K1, N1, P, 'gray')
cp=ax.contour(Y, X, P)
plt.colorbar(cp)
ax.set_xlabel('gamma value')
ax.set_ylabel('eta value')
#ax.set_zlabel('Number of correct predictions')
plt.show()