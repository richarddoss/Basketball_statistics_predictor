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

dataFile=open('screenScraping/RegularSeasonteamstats.csv','r')
reader=csv.reader(dataFile)
j=0
Teams=['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEL','DEN','DET','EST','FCB','GSW','HOU','IND','LAC','LAL','MAC','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','RMD','SAC','SAS','SDS','SLA','TOR','USA','UTA','WAS','WLD','WST']
teams_rating = collections.OrderedDict()
accuracy=0
k=0
check=[]
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
            add=Team1+Team2
            #print("adding stage")
            #print(add)
            #check[k]=add
            #k=k+1
        else:
            Team1=s[0]
            Team2=s[2]
            add = Team2+Team1
            #print("add stage")
            #print(add)
            #check[k] =add
            #k = k + 1
        if row[3]=='W':
            s1=1
            s2=0
        else:
            s1=0
            s2=1
        if (s1==1 and teams_rating[Team1]>teams_rating[Team2]) or(s2==1 and teams_rating[Team2]>teams_rating[Team1]):
            accuracy+=1
        if add in check:
            check.remove(add)
            k=k-1
            #print("chec")
            #print(check)
        else:
            check.insert(0,add)
            k=k+1
            teams_rating[Team1],teams_rating[Team2]=elo(teams_rating[Team1],teams_rating[Team2],20,s1,s2,Team1,Team2)
            #print("chec")
            #print(check)
            print(Team1,"rating",teams_rating[Team1],Team2,"rating",teams_rating[Team2])
    j=j+1
print(accuracy)
for i in range(0,40):
    print(Teams[i],teams_rating[Teams[i]])
EST=['ATL','BOS','BKN','CHA','CHI','CLE','DET','IND','MIA','MIL','NYK','ORL','PHI','TOR','WST']
WST=['LAC','LAL','MEM','MIN','NOP','OKC','SAC','SAS','UTA','GSW','HOU','POR','DAL','DEN','PHX']
#for i in range(0,15):
#    print(WST[i],teams_rating[WST[i]])
TeamRatingEST=np.zeros((15))
TeamRatingWST=np.zeros((15))
for i in range(0,15):
    TeamRatingEST[i]=teams_rating[EST[i]]
    TeamRatingWST[i]=teams_rating[WST[i]]
print(TeamRatingEST)
order1=np.argsort(TeamRatingEST)
order2=np.argsort(TeamRatingWST)
order1=order1[7:15]
order2=order2[7:15]
print(order1)
print(order2)
print("teams making it to the playoffs")
print("From the east conference")
print(EST[order1[7]],EST[order1[6]],EST[order1[5]],EST[order1[4]],EST[order1[3]],EST[order1[2]],EST[order1[1]],EST[order1[0]])
print("From the west conference")
print(WST[order2[7]],WST[order2[6]],WST[order2[5]],WST[order2[4]],WST[order2[3]],WST[order2[2]],WST[order2[1]],WST[order2[0]])
print("first game",EST[order1[7]],"v/s",EST[order1[0]])
print("second game",EST[order1[6]],"v/s",EST[order1[1]])
print("third game",EST[order1[5]],"v/s",EST[order1[2]])
print("fourth game",EST[order1[4]],"v/s",EST[order1[3]])

for i in range(8):
    print(WST[order2[i]],'west')
print("first game",WST[order2[7]],"v/s",WST[order2[0]])
print("second game",WST[order2[6]],"v/s",WST[order2[1]])
print("third game",WST[order2[5]],"v/s",WST[order2[2]])
print("fourth game",WST[order2[4]],"v/s",WST[order2[3]])