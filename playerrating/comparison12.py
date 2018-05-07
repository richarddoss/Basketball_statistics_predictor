from collections import defaultdict
import collections
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
import impactPlayer as i1
import impactWPlayer as i2
rating1=i1.func1()
rating2=i2.func2()
plt.plot(rating1,label='with LeBron James')
plt.plot(rating2,label='without LeBron James')
plt.title("Cleveland Cavaliers performance NBA 2016-17")
plt.legend()
plt.show()