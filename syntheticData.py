import csv
import pandas as pd
import re
import numpy as np
import collections
#from elo import rate_1vs1
def elo(r1,r2,k,s1,s2,Team1,Team2):
    R1=pow(10,r1/400)
    R2=pow(10,r2/400)
    #R2=10^(r2/400)
    E1=R1/(R1+R2)
    E2=R2/(R1+R2)
    print(Team1,"has ",int(E1*100),"%to win")
    print(Team2,"has",int(E2*100),"%to win")
    if s1==1:
        print(Team1 , "won")
        g=0
    else:
        g=1
        print(Team2,"won")
    r1_cap=r1+k*(s1-E1)
    r2_cap=r2+k*(s2-E2)
    return r1_cap,r2_cap

dataFile=open('screenScraping/syntheticDataMatchup.csv','r')
csvFile=open('screenScraping/syntheticData1','w')
writer=csv.writer(csvFile)
reader=csv.reader(dataFile)
writer.writerow(['Team1','Team2','Results'])
j=0
Teams=['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEL','DEN','DET','EST','FCB','GSW','HOU','IND','LAC','LAL','MAC','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','RMD','SAC','SAS','SDS','SLA','TOR','USA','UTA','WAS','WLD','WST']
prior1=[1000,1010,1020,1030,1040,1050,1060,1070,1080,1090,1100,1110,1120,1130,1140,1150,1160,1170,1180,1190,1200,1210,1220,1230,1240,1250,1260,1270,1280,1290,1300,1310,1320,1330,1340,1350,1360,1370,1380,1390]
teams_rating = collections.OrderedDict()
prior=collections.OrderedDict()
for i in range(0,40):
    prior[Teams[i]]=prior1[i]

accuracy=0
k=0
check=[]
for i in range(0,40):
    teams_rating[Teams[i]]=1000
for row in reader:
    if j!=0:
        Team1=row[0]
        Team2=row[1]
        Team1Rating=np.random.normal(prior[Team1],200,1)
        Team2Rating = np.random.normal(prior[Team2], 200, 1)
        print("team1",Team1Rating)
        print("team2",Team2Rating)
        if Team1Rating>Team2Rating:
            row1=[row[0],row[1],'W']
        else:
            row1=[row[0],row[1],'L']
        writer.writerow(row1)
    j=j+1
print(accuracy)
csvFile.close()
dataFile.close()