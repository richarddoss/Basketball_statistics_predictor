import csv
import re
import numpy as np
import collections
import time
import statGeneration
def elo(r1,r2,k,s1,s2,Team1,Team2):
    R1=pow(10,r1/400)
    R2=pow(10,r2/400)
    #R2=10^(r2/400)
    E1=R1/(R1+R2)
    E2=R2/(R1+R2)
   # print(Team1,"has ",int(E1*100),"%to win")
    #print(Team2,"has",int(E2*100),"%to win")
    #if s1==1:
    #    print(Team1 , "won")
   # else:
    #    print(Team2,"won")
    r1_cap=r1+k*(s1-E1)
    r2_cap=r2+k*(s2-E2)
    return r1_cap,r2_cap

def estimate1(K):
    dataFile=open('MatchupGenerate.csv','r')
    reader=csv.reader(dataFile)
    j=0
    flag=0
    Teams=collections.OrderedDict()
    for i in range(0,16):
        Teams[i]="T"+str(i+1)
    teams_rating = collections.OrderedDict()
    accuracy=0
    for i in range(0,16):
        teams_rating[Teams[i]]=1000
    for row in reader:
        if j!=0:
            s=re.split('\W+',row[0])
            #print(s)
            Team1="T"+str(s[0])
            Team2="T"+str(s[3])
            if row[2]=='W':
                s1=1
                s2=0
            else:
                s1=0
                s2=1
            if (s1==1 and teams_rating[Team1]>(teams_rating[Team2])) or(s2==1 and (teams_rating[Team2])>teams_rating[Team1]):
                accuracy+=1
            teams_rating[Team1],teams_rating[Team2]=elo(teams_rating[Team1],teams_rating[Team2],K,s1,s2,Team1,Team2)
            #print(Team1,"rating",teams_rating[Team1],Team2,"rating",teams_rating[Team2])
            #time.sleep(2)
            j=j+1
        else:
            j=1
    print("ESTIMATED WITH CONVENTIONAL")
    print("Correct Predicitons",accuracy,"Total Number of games",j-1)
    return teams_rating,accuracy
