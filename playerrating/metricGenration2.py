from collections import defaultdict
import collections
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np

def logistic(x):
    y = 1 / (1 + pow(10, -(x) / 40))
    return (y)
def elo(playerRating, minutesPlayed, Team1, Team2, TotTime, plusminus1,plusminus2,x1,x2):
    m1 = 0
    m2 = 0
    NumOfPlayer = 0
    Sum = 0
    K = 500
    Offset = defaultdict(dict)
    actualValue = defaultdict(dict)
    expectedValue = defaultdict(dict)
    Total1=0
    Total2=0
    for players in minutesPlayed[Team1]:
        #print("Minutes Played",minutesPlayed[Team1][players],players)
        m1 += playerRating[players] * minutesPlayed[Team1][players]
        Total1+=minutesPlayed[Team1][players]
    for players in minutesPlayed[Team2]:
        m2 += playerRating[players] * minutesPlayed[Team2][players]
        Total2 += minutesPlayed[Team2][players]
    #print(Total1,Total2,"AAAAAAAAAA",TotTime)
    #time.sleep(2)
    w1=0
    w2=0
    for fixedPlayer in minutesPlayed[Team1]:
        new = TotTime - minutesPlayed[Team1][fixedPlayer]*TotTime
        m1without = ((m1 - playerRating[fixedPlayer] * minutesPlayed[Team1][fixedPlayer]) * TotTime) / new
        minPlayedByPlayer = minutesPlayed[Team1][fixedPlayer]  # *int(TotTime)
        #print(minPlayedByPlayer, fixedPlayer)
        PtTeam = minPlayedByPlayer * playerRating[fixedPlayer] + 4 * minPlayedByPlayer * m1without
        PtOppTeam = minPlayedByPlayer * 5 * m2
        #print("Player Rating",playerRating[fixedPlayer],"Rest of the team",m1without,"Opp Team strength",m2)
        #time.sleep(2)
        X = round(PtTeam - PtOppTeam)
        X=X*(TotTime/2500)
        x1.append(X)
        x2.append(plusminus1[fixedPlayer])
        #expectedValue[fixedPlayer] = round(logistic(X), 2)
        #actualValue[fixedPlayer] = round(logistic(plusminus1[fixedPlayer]), 2)
        #print(fixedPlayer,minPlayedByPlayer,plusminus1[fixedPlayer],X)
        PtDiff=plusminus1[fixedPlayer]-X
        #print("Actual score",plusminus1[fixedPlayer],"Expected Score",X,"Strength",X/minPlayedByPlayer)
        #time.sleep(2)
        #Offset[fixedPlayer] = K * (actualValue[fixedPlayer] - expectedValue[fixedPlayer])
        Offset[fixedPlayer] = K * (round(logistic(PtDiff),2))
        Sum = Sum + minPlayedByPlayer*Offset[fixedPlayer]
        NumOfPlayer = NumOfPlayer + 1
        w1+=minPlayedByPlayer
    # calculating offset for Team2
    for fixedPlayer in minutesPlayed[Team2]:
        new = TotTime - minutesPlayed[Team2][fixedPlayer]
        m2without = ((m2 - playerRating[fixedPlayer] * minutesPlayed[Team2][fixedPlayer]) * TotTime) / new
        minPlayedByPlayer = minutesPlayed[Team2][fixedPlayer]  # *int(TotTime)
        #print(minPlayedByPlayer,fixedPlayer)
        PtTeam = minPlayedByPlayer * playerRating[fixedPlayer] + 4 * minPlayedByPlayer * m2without
        PtOppTeam = minPlayedByPlayer * 5 * m1
        #print("Player Rating", playerRating[fixedPlayer], "Rest of the team", m1without, "Opp Team strength", m2)
        #time.sleep(2)
        X = round(PtTeam - PtOppTeam)
        X = X * (TotTime / 2500)
        x1.append(X)
        x2.append(plusminus2[fixedPlayer])
        #print(fixedPlayer, minPlayedByPlayer, plusminus2[fixedPlayer], X)
        #expectedValue[fixedPlayer] = round(logistic(X), 2)
        #actualValue[fixedPlayer] = round(logistic(plusminus2[fixedPlayer]), 2)
        PtDiff = plusminus2[fixedPlayer] - X
        #print("Actual score", plusminus2[fixedPlayer], "Expected Score", X,"Strength",X/minPlayedByPlayer)
        #time.sleep(2)
        #Offset[fixedPlayer] = K * (actualValue[fixedPlayer] - expectedValue[fixedPlayer])
        Offset[fixedPlayer] = K * (round(logistic(PtDiff), 2))
        Sum = Sum + minPlayedByPlayer*Offset[fixedPlayer]
        NumOfPlayer = NumOfPlayer + 1
        w2+=minPlayedByPlayer

    #mean = Sum / NumOfPlayer
    #weightedmean= Sum
    # Updating the player ratings
    print("next phase")
    sum=0
    offset=0
    for fixedPlayer in minutesPlayed[Team1]:
        #Offset[fixedPlayer] = round(Offset[fixedPlayer] - mean)
        Offset[fixedPlayer]=minutesPlayed[Team1][fixedPlayer]*(2*Offset[fixedPlayer]-Sum)
        #print("offset", Offset[fixedPlayer])
        playerRating[fixedPlayer] = playerRating[fixedPlayer] + Offset[fixedPlayer]
        offset=Offset[fixedPlayer]+offset
        sum=sum+playerRating[fixedPlayer]
    for fixedPlayer in minutesPlayed[Team2]:
        #Offset[fixedPlayer] = round(Offset[fixedPlayer] - mean)
        Offset[fixedPlayer] = minutesPlayed[Team2][fixedPlayer] * (2 * Offset[fixedPlayer] - Sum)
        #print("offset", Offset[fixedPlayer])
        playerRating[fixedPlayer] = playerRating[fixedPlayer] + Offset[fixedPlayer]
        offset = Offset[fixedPlayer] + offset
        sum=sum+playerRating[fixedPlayer]
    #print("The sum of the players",sum,NumOfPlayer,sum/NumOfPlayer)
    print("Sum",Sum)
    print("Sum of offsets",offset)
    print("w1+w2",w1+w2)
    time.sleep(2)
    return playerRating,x1,x2


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
x1=[]
x2=[]
avg=[]
number=0
flag=0
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
        '''else:
            Team1 = s[0]
            Team2 = s[2]
            print(s[1])
            time.sleep(2)
            c = Team2 + Team1
        '''
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
                            minutesPlayed[Team1][row2[0]] = int(row2[5]) / (int(row1[4]))
                            plusminus1[row2[0]] = int(row2[7])
                            if check[row2[0]] == {}:
                                playerRating[row2[0]] = 1000
                                check[row2[0]] = 'Filled'
                        elif Team2==row2[1]:
                            minutesPlayed[Team2][row2[0]] = int(row2[5]) / (int(row1[4]))
                            plusminus2[row2[0]] = int(row2[7])
                            if check[row2[0]] == {}:
                                playerRating[row2[0]] = 1000
                                check[row2[0]] = 'Filled'
                        else:
                            print("HHHHHHHHHEEEEEEEEEEELLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                j = j + 1
            j = 0
            csv_file2.close()
            checklist.append(c)
            for fixedPlayer in minutesPlayed[Team1]:
                if minutesPlayedEstimate[fixedPlayer] == {}:
                    print(fixedPlayer)
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
            print("%%%%%%%%%%%%%%%%%  Before Update %%%%%%%%%%%%%%%%")
            print("Updated rating for {}".format(Team1), round(p1))
            print("updated rating for {}".format(Team2), round(p2))
            print("total",p1+p2)
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
            #if Team1 == 'LAC' or Team2 == 'LAC':
            match = match + 1
            print(Team1, row1[3], Team2, noOfPredictions, match,"Prediction Rate",noOfPredictions/match)
            #print("random")
            duplicate = playerRating
            playerRating,x1,x2 = elo(playerRating, minutesPlayed, Team1, Team2, int(row1[4]), plusminus1, plusminus2,x1,x2)
            m1 = 0
            m2 = 0
            p1=0
            p2=0
            for players in minutesPlayed[Team1]:
                m1 += playerRating[players] * minutesPlayed[Team1][players]
                p1+=playerRating[players]
            for players in minutesPlayed[Team2]:
                m2 += playerRating[players] * minutesPlayed[Team2][players]
                p2+=playerRating[players]
            TeamRating[Team1] = p1
            TeamRating[Team2] = p2

            print("%%%%%%%%%%%% after update%%%%%%%%%%%%%%%")
            print("Updated rating for {}".format(Team1), round(p1))
            print("updated rating for {}".format(Team2), round(p2))
            print("total",p1+p2)
            #time.sleep(2)
            #print("Match number", match)
            sumTeam = 0
            for Teeam in TeamRating:
                sumTeam = sumTeam + TeamRating[Teeam]
            print("Sum of team rating", sumTeam)
            #time.sleep(2)
            if match == 1230:
                print(sorted(TeamRating.values()))
                print(TeamRating)
                sumTeam=0
                for Teeam in TeamRating:
                    sumTeam = sumTeam + TeamRating[Teeam]
                #print("Sum of team rating", sumTeam)
        # time.sleep(4)
        '''else:
            # print("Trying to repeat")
            # time.sleep(10)
            checklist.remove(c)
        '''

    # print("NEXT ROUND")
    i = i + 1
#x1=np.array(x1)
#x2=np.array(x2)
#plt.scatter(x1.reshape(-1,1), x2.reshape(-1,1),  color='purple')
#plt.show()
print("&&&&&")
SUM=sum(avg)
print("average",SUM/number)
csv_file1.close()
csv_file2.close()

