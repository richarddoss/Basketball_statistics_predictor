import collections
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
import train_test as t
import eloTrails as e

PRED1=e.func1()
PRED2=t.func2()
plt.plot(PRED1,label="Elo algo")
plt.plot(PRED2,label="Proposed algo")
plt.xlabel("MATCH NUMBER")
plt.ylabel("PREDICTION RATE")
plt.legend()
plt.title("NBA regular season 2017-18")
plt.show()