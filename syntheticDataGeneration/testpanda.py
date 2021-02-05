import pandas
import numpy as np
import panda as p
p.estimate(10)
'''
filename='MatchupGenerate.csv'
filename2='playerstats.csv'
csv_delimiter = ' '
df = pandas.read_csv(filename)
df2= pandas.read_csv(filename2)
data = df.values
#df3=df2.loc[df2["matchnumber"]==1]
#print("heelo")
#print(df3.loc[df3["Team"]=="T10"])
data1=df2.loc[df2["matchnumber"]==1]
data2=data1.loc[data1["Team"]=="T10"]
print(np.shape(data2))
'''