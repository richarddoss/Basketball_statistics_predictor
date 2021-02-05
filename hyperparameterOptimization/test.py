from collections import defaultdict
import collections
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
import function as f
import sklearn.metrics as m
import pickle
K=[1,2,5,10,20,30,50,100,200,500]
def P(r1,r2):
    R1 = pow(10, r1 / 400)
    R2 = pow(10, r2 / 400)
    E1 = R1 / (R1 + R2)
    return(E1,1-E1)

teams_rating = collections.OrderedDict()
Teams=['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEL','DEN','DET','EST','FCB','GSW','HOU','IND','LAC','LAL','MAC','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','RMD','SAC','SAS','SDS','SLA','TOR','USA','UTA','WAS','WLD','WST']

for k in range(10):
    accuracy=0
    j=0
    y_pred=[]
    y_true=[]
    csv_file1 = open('TeamMatchups2015-16.csv', 'r')
    reader1 = csv.reader(csv_file1)
    for i in range(0, 40):
        teams_rating[Teams[i]] = 1000
    ### Training phase
    for row in reader1:
        if j != 0:
            s = re.split('\W+', row[2])
            if len(s) == 2:
                #print("Match", j)
                Team1 = s[0]
                Team2 = s[1]
                if row[3] == 'W':
                    s1 = 1
                    s2 = 0
                else:
                    s1 = 0
                    s2 = 1
                #if (s1 == 1 and teams_rating[Team1] > (teams_rating[Team2] + 100)) or (s2 == 1 and (100 + teams_rating[Team2]) > teams_rating[Team1]):
                    #accuracy += 1
                r1=teams_rating[Team1]
                r2=teams_rating[Team2]+100
                #y_true.append(s1)
                #p=P(r1,r2)
                #y_pred.append(p)
                teams_rating[Team1], teams_rating[Team2] = f.elo(teams_rating[Team1], teams_rating[Team2] , K[k], s1, s2, Team1, Team2)
                #print(Team1, "rating", teams_rating[Team1], Team2, "rating", teams_rating[Team2])
                # time.sleep(2)
                j = j + 1
        else:
            j = 1
    csv_file1 = open('TeamMatchups.csv', 'r')
    reader1 = csv.reader(csv_file1)
    j=0
    accuracy=0
    for row in reader1:
        if j != 0 and j<=615:
            s = re.split('\W+', row[2])
            #print(s)
            if len(s) == 2:
                #print("Match", j)
                Team1 = s[0]
                Team2 = s[1]
                if row[3] == 'W':
                    s1 = 1
                    s2 = 0
                else:
                    s1 = 0
                    s2 = 1
                r1 = teams_rating[Team1]
                r2 = teams_rating[Team2]+100
                #if (s1 == 1 and teams_rating[Team1] > (teams_rating[Team2] + 100)) or (s2 == 1 and (100 + teams_rating[Team2]) > teams_rating[Team1]):
                    #accuracy += 1
                #y_true.append(s1)
                #p=P(r1,r2)
                #y_pred.append(p)
                teams_rating[Team1], teams_rating[Team2] = f.elo(teams_rating[Team1], teams_rating[Team2], K[k], s1, s2, Team1, Team2)
                #print(Team1, "rating", teams_rating[Team1], Team2, "rating", teams_rating[Team2])
                # time.sleep(2)
                j = j + 1
        elif j>615:
            ##### Validation phase
            s = re.split('\W+', row[2])
            if len(s) == 2:
                # print("Match", j)
                Team1 = s[0]
                Team2 = s[1]
                if row[3] == 'W':
                    s1 = 1
                    s2 = 0
                    add=0
                else:
                    add=1
                    s1 = 0
                    s2 = 1
                r1 = teams_rating[Team1]
                r2 = teams_rating[Team2]+100
                if (s1 == 1 and r1 > r2 ) or (s2 == 1 and r2 > r1):
                    accuracy += 1
                y_true.append(s1)
                p = P(r1, r2)
                y_pred.append(p)
                teams_rating[Team1], teams_rating[Team2] = f.elo(teams_rating[Team1], teams_rating[Team2], K[k], s1, s2,
                                                                 Team1, Team2)
                # print(Team1, "rating", teams_rating[Team1], Team2, "rating", teams_rating[Team2])
                # time.sleep(2)
                j = j + 1
        else:
            j = 1
    #print(np.shape(y_true),np.shape(y_pred))
    print("K value",K[k],"Log loss",f.logLoss(y_true,y_pred),"accuracy",accuracy)

# Testing phase with k=30
accuracy=0
j=0
y_pred=[]
y_true=[]
csv_file1 = open('TeamMatchups2017-18.csv', 'r')
reader1 = csv.reader(csv_file1)
PRED=[]
for row in reader1:
    if j != 0:
        s = re.split('\W+', row[2])
        if len(s) == 2:
            #print("Match", j)
            Team1 = s[0]
            Team2 = s[1]
            if row[3] == 'W':
                s1 = 1
                s2 = 0
                add=0
            else:
                add=1
                s1 = 0
                s2 = 1
            r1 = teams_rating[Team1]
            r2 = teams_rating[Team2] + 100
            if (s1 == 1 and r1 > r2) or (s2 == 1 and r2 > r1):
                accuracy += 1
            y_true.append(s1)
            p=P(r1,r2)
            y_pred.append(p)
            teams_rating[Team1], teams_rating[Team2] = f.elo(teams_rating[Team1], teams_rating[Team2], 100, s1, s2, Team1, Team2)
            PRED.append(round(accuracy/j,2))
            #print(Team1, "rating", teams_rating[Team1], Team2, "rating", teams_rating[Team2])
            #time.sleep(2)
            j = j + 1
    else:
        j = 1
print("K value",30,"Log loss",f.logLoss(y_true,y_pred),"accuracy",accuracy)
pickle_out = open("PREDK3","wb")
pickle.dump(PRED,pickle_out)
pickle_out.close()