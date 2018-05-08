from collections import defaultdict
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
import function as f
from mpl_toolkits import mplot3d
import pickle
f = open("PRED1",'rb')
PRED1=pickle.load(f)
f = open("PRED2",'rb')
PRED2=pickle.load(f)

plt.plot(PRED1,label="Elo algorithm")
plt.plot(PRED2,label="proposed algorithm")
#ax.plot3D(K1, N1, P, 'gray')
#cp=ax.contour(Y, X, P)
#plt.colorbar(cp)
plt.xlabel('Number of Matches')
plt.ylabel('Prediction Rate')
plt.legend()
#ax.set_zlabel('Number of correct predictions')
plt.show()