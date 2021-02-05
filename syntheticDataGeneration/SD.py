from collections import defaultdict
import collections
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np

csv_file1 = open('PlayerDetails.csv', 'r')
reader1 = csv.reader(csv_file1)
time=[]
name='Stephen Curry'
for row in reader1:
    if row[0]==name:
        time.append(int(row[5]))
print("Standard Deviation of ",name,np.std(time))
