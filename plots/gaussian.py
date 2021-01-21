import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm
import numpy as np
def logistic(x):
    y = (1 / (1 + pow(10, -(x) / 400)))
    return (y)
from scipy.stats import norm
ax=plt.axes(frameon=False)
x=np.linspace(-1000,4000,500)
x1=plt.plot(x,norm.pdf(x,1500,400),label='Team 1 strength')
x2=plt.plot(x,norm.pdf(x,1900,400),label='Team 2 strength')
#x2=np.linspace(0,1400,500)
#x1=plt.plot(x,logistic(x),label='logisitc')
#x3=plt.plot(x,norm.cdf(x/400),label='normal distribution')
#plt.fill_between(x2,mlab.normpdf(x2,-400,np.sqrt(2)*400),facecolor='red')
#x2=plt.plot(x,mlab.normpdf(x,1900,400),label='player2 strength')
plt.xlabel("team performance")
ax.axes.get_yaxis().set_visible(False)
plt.legend()
#plt.show()
plt.savefig("mygraph.png")
