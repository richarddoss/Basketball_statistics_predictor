import numpy as np
import matplotlib.pyplot as plt
def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
x=np.linspace(-2000,1500,150)
y=[]
for i in range(0,150):
    y.append(-150*gaussian(x[i],0,400)+200)
y=np.array(y)
plt.plot(x.reshape(-1,1),y.reshape(-1,1),color='red')
plt.show()

