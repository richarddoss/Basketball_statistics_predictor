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
    else:
        print(Team2,"won")
    r1_cap=r1+k*(s1-E1)
    r2_cap=r2+k*(s2-E2)
    return r1_cap,r2_cap

dataFile=open('screenScraping/Totalteamstats.csv','r')
reader=csv.reader(dataFile)
j=0
Teams=['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEL','DEN','DET','EST','FCB','GSW','HOU','IND','LAC','LAL','MAC','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','RMD','SAC','SAS','SDS','SLA','TOR','USA','UTA','WAS','WLD','WST']
teams_rating = collections.OrderedDict()
accuracy=0
for i in range(0,40):
    teams_rating[Teams[i]]=1000
for row in reader:
    if j!=0:
        print("\n")
        print("Match",j)
        s=re.split('\W+',row[2])
        if len(s)==2:
            Team1=s[0]
            Team2=s[1]
        else:
            Team1=s[0]
            Team2=s[2]
        if row[3]=='W':
            s1=1
            s2=0
        else:
            s1=0
            s2=1
        if (s1==1 and teams_rating[Team1]>teams_rating[Team2]) or(s2==1 and teams_rating[Team2]>teams_rating[Team1]):
            accuracy+=1
        teams_rating[Team1],teams_rating[Team2]=elo(teams_rating[Team1],teams_rating[Team2],32,s1,s2,Team1,Team2)
        print(Team1,"rating",teams_rating[Team1],Team2,"rating",teams_rating[Team2])
    j=j+1
print(accuracy/2829)
#for i in range(0,40):
    #print(Teams[i],teams_rating[Teams[i]])
#print(j)