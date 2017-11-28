import csv
import pandas as pd
import re
import numpy as np
import collections
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

dataFile=open('screenScraping/syntheticData1.csv','r')
reader=csv.reader(dataFile)
j=0
Teams=['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEL','DEN','DET','EST','FCB','GSW','HOU','IND','LAC','LAL','MAC','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','RMD','SAC','SAS','SDS','SLA','TOR','USA','UTA','WAS','WLD','WST']
#prior=[1000,1010,1020,1030,1040,1050,'D,'DEL','DEN','DET','EST','FCB','GSW','HOU','IND','LAC','LAL','MAC','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','RMD','SAC','SAS','SDS','SLA','TOR','USA','UTA','WAS','WLD','WST']
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
        Team1=row[0]
        Team2=row[1]
        if row[2]=='W':
            s1=1
            s2=0
        else:
            s1=0
            s2=1
        if (s1==1 and teams_rating[Team1]>teams_rating[Team2]) or(s2==1 and teams_rating[Team2]>teams_rating[Team1]):
            accuracy+=1

        teams_rating[Team1],teams_rating[Team2]=elo(teams_rating[Team1],teams_rating[Team2],20,s1,s2,Team1,Team2)
        print(Team1,"rating",teams_rating[Team1],Team2,"rating",teams_rating[Team2])
    j=j+1
print(accuracy)
dataFile.close()
#Bracket Formation
for i in range(0,40):
    print(Teams[i],teams_rating[Teams[i]])
EST=['ATL','BOS','BKN','CHA','CHI','CLE','DET','IND','MIA','MIL','NYK','ORL','PHI','TOR','WST']
WST=['LAC','LAL','MEM','MIN','NOP','OKC','SAC','SAS','UTA','GSW','HOU','POR','DAL','DEN','PHX']
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
Brackets=["1","2","3","4","5","6","7","8"]
Brackets2=["1","2","3","4","5","6","7","8"]
FinalsBracket=["" for x in range(31)]
f=-1
for indx in range(8):
    Brackets[indx]=EST[order1[7-indx]]
h=4
while h!=0:
    for q in range(0,h):
        print(Brackets[h*2-1-q],"v/s",Brackets[q])
        if teams_rating[Brackets[h*2-1-q]] < teams_rating[Brackets[q]]:
            Brackets[q]=Brackets[q]
            print(Brackets[q],"won")
            f = f + 1
            FinalsBracket[f]=Brackets[2*h-1-q]
            f=f+1
            FinalsBracket[f]=Brackets[q]
        else:
            Brackets[q]=Brackets[h*2-1-q]
            print(Brackets[q],"won")
            f = f + 1
            FinalsBracket[f] = Brackets[2 * h - 1 - q]
            f = f + 1
            FinalsBracket[f] = Brackets[q]

    h=int(h/2)
print("finals season in western confernece")
#For western conferences
for indx in range(8):
    Brackets2[indx]=WST[order2[7-indx]]
h=4
while h!=0:
    for q in range(0,h):
        print(Brackets2[h*2-1-q],"v/s",Brackets2[q])
        if teams_rating[Brackets2[h*2-1-q]] < teams_rating[Brackets2[q]]:
            Brackets2[q]=Brackets2[q]
            print(Brackets2[q],"won")
            f = f + 1
            FinalsBracket[f] = Brackets2[2 * h - 1 - q]
            f = f + 1
            FinalsBracket[f] = Brackets2[q]
        else:
            Brackets2[q]=Brackets2[h*2-1-q]
            print(Brackets2[q],"won")
            f = f + 1
            FinalsBracket[f] = Brackets2[2 * h - 1 - q]
            f = f + 1
            FinalsBracket[f] = Brackets2[q]
    h = int(h / 2)
"FInals!!!"
print(teams_rating[Brackets[0]],teams_rating[Brackets2[0]])
if teams_rating[Brackets[0]]>teams_rating[Brackets2[0]]:
    f = f + 1
    FinalsBracket[f] = Brackets[0]
    f = f + 1
    FinalsBracket[f] = Brackets2[0]
    f=f+1
    FinalsBracket[f] = Brackets[0]
else:
    f = f + 1
    FinalsBracket[f] = Brackets[0]
    f = f + 1
    FinalsBracket[f] = Brackets2[0]
    f = f + 1
    FinalsBracket[f] = Brackets2[0]
print(FinalsBracket)



