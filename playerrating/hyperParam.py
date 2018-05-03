

from collections import defaultdict
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
import function as f
from mpl_toolkits import mplot3d
import pickle
K=[50,150,500,1000]
N=[500,1000,2500,5000,7500,10000]
no=0
P=np.zeros((4,6))
K1=np.zeros(24)
N1=np.zeros(24)
for k in range(4):
    for n in range(6):
        csv_file1 = open('TeamMatchups.csv', 'r')
        reader1 = csv.reader(csv_file1)
        i = 0
        j = 0
        noOfPredictions = 0
        minutesPlayed = defaultdict(dict)
        minutesPlayedEstimate = defaultdict(dict)
        NumberMinutes=defaultdict(dict)
        playerRating = defaultdict(dict)
        plusminus = defaultdict(dict)
        duplicate = defaultdict(dict)
        tempTeam = defaultdict(dict)
        check = defaultdict(dict)
        TeamRating = defaultdict(dict)
        HomeAdv = defaultdict(dict)
        checklist = []
        flog = 1
        match = 0
        avg=[]
        number=0
        flag = 0
        for row1 in reader1:
            plusminus1 = defaultdict(dict)
            plusminus2 = defaultdict(dict)
            if i > 0:
                s = re.split('\W+', row1[2])
                # print(s)
                if len(s) == 2:
                    Team1 = s[0]
                    Team2 = s[1]
                    flag=1
                    c = Team1 + Team2
                    HomeAdv[Team1]=0
                    HomeAdv[Team2]=100
                if (flag==1):
                    flag=0
                    for fixedPlayer in minutesPlayed[Team1]:
                        minutesPlayed[Team1][fixedPlayer] = 0
                        plusminus1[fixedPlayer]=0
                    for fixedPlayer in minutesPlayed[Team2]:
                        minutesPlayed[Team2][fixedPlayer] = 0
                        plusminus2[fixedPlayer]=0
                    csv_file2 = open('PlayerDetails.csv', 'r')
                    reader2 = csv.reader(csv_file2)
                    for row2 in reader2:
                        if j > 0:

                            if (Team1 == row2[1] or Team2 == row2[1]) and row1[1] == row2[2]:
                                # print(row2[0],"playername",row2[1],"team",row2[2],"date")
                                # time.sleep(2)
                                if int(row2[5])!=0:
                                    avg.append(int(row2[6])/int(row2[5]))
                                    number+=1
                                if Team1 == row2[1]:
                                    minutesPlayed[Team1][row2[0]+Team1] = int(row2[5]) / (int(row1[4]))
                                    plusminus1[row2[0]+Team1] = int(row2[7])
                                    if check[row2[0]+Team1] == {}:
                                        playerRating[row2[0]+Team1] = 1000
                                        #print(row2[0])
                                        check[row2[0]+Team1] = 'Filled'
                                elif Team2==row2[1]:
                                    minutesPlayed[Team2][row2[0]+Team2] = int(row2[5]) / (int(row1[4]))
                                    plusminus2[row2[0]+Team2] = int(row2[7])
                                    if check[row2[0]+Team2] == {}:
                                        playerRating[row2[0]+Team2] = 1000
                                        #print(row2[0])
                                        check[row2[0]+Team2] = 'Filled'
                                else:
                                    print("HHHHHHHHHEEEEEEEEEEELLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                        j = j + 1
                    j = 0
                    csv_file2.close()
                    checklist.append(c)
                    for fixedPlayer in minutesPlayed[Team1]:
                        if minutesPlayedEstimate[fixedPlayer] == {}:
                            #print(fixedPlayer)
                            minutesPlayedEstimate[fixedPlayer] = minutesPlayed[Team1][fixedPlayer]
                            NumberMinutes[fixedPlayer] = 1
                        else:
                            minutesPlayedEstimate[fixedPlayer] = (NumberMinutes[fixedPlayer] * minutesPlayedEstimate[fixedPlayer] +
                                                              minutesPlayed[Team1][fixedPlayer]) / (NumberMinutes[fixedPlayer] + 1)
                            NumberMinutes[fixedPlayer] = NumberMinutes[fixedPlayer] + 1
                    for fixedPlayer in minutesPlayed[Team2]:
                        if minutesPlayedEstimate[fixedPlayer] == {}:
                            minutesPlayedEstimate[fixedPlayer] = minutesPlayed[Team2][fixedPlayer]
                            NumberMinutes[fixedPlayer] = 1
                        else:
                            minutesPlayedEstimate[fixedPlayer] = (NumberMinutes[fixedPlayer] * minutesPlayedEstimate[fixedPlayer] +
                                                              minutesPlayed[Team2][fixedPlayer]) / (NumberMinutes[fixedPlayer] + 1)
                            NumberMinutes[fixedPlayer] = NumberMinutes[fixedPlayer] + 1

                    # rating update for the 2 teams
                    m1 = 0
                    m2 = 0
                    p1=0
                    p2=0
                    for players in minutesPlayed[Team1]:
                        m1 += playerRating[players] * minutesPlayedEstimate[players]
                        p1+=playerRating[players]
                    for players in minutesPlayed[Team2]:
                        m2 += playerRating[players] * minutesPlayedEstimate[players]
                        p2+=playerRating[players]
                    #print("%%%%%%%%%%%%%%%%%  Before Update %%%%%%%%%%%%%%%%")
                    #print("Updated rating for {}".format(Team1), round(p1))
                    #print("updated rating for {}".format(Team2), round(p2))
                    #print("p2",p2)
                    #print("total1",p1+p2)
                    sumTeam = 0
                    for Teeam in minutesPlayed:
                        for player in minutesPlayed[Teeam]:
                            sumTeam = sumTeam + playerRating[player]
                            # print(Teeam,TeamRating[Teeam])
                    #print(Team1,p1)
                    #print(Team2,p2)
                    #print("total1",p1+p2)
                    #print("Sum of team rating1", sumTeam)
                    #time.sleep(2)
                    m1+=HomeAdv[Team1]
                    m2 += HomeAdv[Team2]
                    if m1 > m2:
                        outcome = 'W'
                    else:
                        outcome = 'L'
                    if outcome == row1[3]:
                        noOfPredictions = noOfPredictions + 1
                        W = 1
                    else:
                        W = 0
                    match = match + 1
                    if match==1230:
                        print(K[k], N[n], noOfPredictions, match,"Prediction Rate",noOfPredictions/match)
                        P[k][n]=(noOfPredictions/match)*100
                        K1[no]=K[k]
                        N1[no]=N[n]
                        no+=1
                    playerRating= f.elo(playerRating, minutesPlayed, Team1, Team2, int(row1[4]), plusminus1, plusminus2,K[k],N[n])
                    m1 = 0
                    m2 = 0
                    p1=0
                    p2=0
                    for players in minutesPlayed[Team1]:
                        m1 += playerRating[players] * minutesPlayedEstimate[players]
                        p1+=playerRating[players]
                    for players in minutesPlayed[Team2]:
                        m2 += playerRating[players] * minutesPlayedEstimate[players]
                        p2+=playerRating[players]
                    TeamRating[Team1] = m1
                    TeamRating[Team2] = m2

            i = i + 1
        SUM=sum(avg)    # computing the constant value
        #print("average",SUM/number)
        csv_file1.close()
        #print(Dray)
fig = plt.figure()
pickle_out = open("K1","wb")
pickle.dump(K,pickle_out)
pickle_out.close()
pickle_out = open("N1","wb")
pickle.dump(N,pickle_out)
pickle_out.close()
pickle_out = open("P","wb")
pickle.dump(P,pickle_out)
pickle_out.close()
#ax = plt.axes(projection='3d')
#ax.plot3D(K1, N1, P, 'gray')
#ax.contour3D(K1, N1, P, 50, cmap='green')
#ax.set_xlabel('gamma value')
#ax.set_ylabel('eta value')
#ax.set_zlabel('Number of correct predictions')