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
def elo(playerRating, minutesPlayed, Team1, Team2, TotTime, plusminus1,plusminus2):
    m1 = 0
    m2 = 0
    NumOfPlayer = 0
    Sum = 0
    K = 500
    Offset = defaultdict(dict)
    for players in minutesPlayed[Team1]:
        #print("Minutes Played",minutesPlayed[Team1][players],players)
        m1 += playerRating[players] * minutesPlayed[Team1][players]
    for players in minutesPlayed[Team2]:
        #print("Minutes Played111", minutesPlayed[Team2][players], players)
        m2 += playerRating[players] * minutesPlayed[Team2][players]
    w1=0
    w2=0
    for fixedPlayer in minutesPlayed[Team1]:
        new = TotTime - minutesPlayed[Team1][fixedPlayer]*TotTime
        m1without = ((m1 - playerRating[fixedPlayer] * minutesPlayed[Team1][fixedPlayer]) * TotTime) / new
        minPlayedByPlayer = minutesPlayed[Team1][fixedPlayer]  # *int(TotTime)
        PtTeam = minPlayedByPlayer * playerRating[fixedPlayer] + 4 * minPlayedByPlayer * m1without
        PtOppTeam = minPlayedByPlayer * 5 * m2
        X = round(PtTeam - PtOppTeam)
        X=X*(TotTime/2500)
        PtDiff=plusminus1[fixedPlayer]-X
        Offset[fixedPlayer] = K * (round(logistic(PtDiff),2))
        Sum = Sum + minPlayedByPlayer*Offset[fixedPlayer]
        NumOfPlayer = NumOfPlayer + 1
        w1+=minPlayedByPlayer
    # calculating offset for Team2
    for fixedPlayer in minutesPlayed[Team2]:
        new = TotTime - minutesPlayed[Team2][fixedPlayer]
        m2without = ((m2 - playerRating[fixedPlayer] * minutesPlayed[Team2][fixedPlayer]) * TotTime) / new
        minPlayedByPlayer = minutesPlayed[Team2][fixedPlayer]  # *int(TotTime)
        PtTeam = minPlayedByPlayer * playerRating[fixedPlayer] + 4 * minPlayedByPlayer * m2without
        PtOppTeam = minPlayedByPlayer * 5 * m1
        X = round(PtTeam - PtOppTeam)
        X = X * (TotTime / 2500)
        PtDiff = plusminus2[fixedPlayer] - X
        Offset[fixedPlayer] = K * (round(logistic(PtDiff), 2))
        Sum = Sum + minPlayedByPlayer*Offset[fixedPlayer]
        NumOfPlayer = NumOfPlayer + 1
        w2+=minPlayedByPlayer
    # Updating the player ratings
    #print("next phase")
    sum=0
    offset=0
    for fixedPlayer in minutesPlayed[Team1]:
        Offset[fixedPlayer]=minutesPlayed[Team1][fixedPlayer]*(2*Offset[fixedPlayer]-Sum/w1)
        playerRating[fixedPlayer] = playerRating[fixedPlayer] + Offset[fixedPlayer]
        offset=Offset[fixedPlayer]+offset
        sum=sum+playerRating[fixedPlayer]
    for fixedPlayer in minutesPlayed[Team2]:
        Offset[fixedPlayer] = minutesPlayed[Team2][fixedPlayer] * (2 * Offset[fixedPlayer] - Sum/w2)
        playerRating[fixedPlayer] = playerRating[fixedPlayer] + Offset[fixedPlayer]
        offset = Offset[fixedPlayer] + offset
        sum=sum+playerRating[fixedPlayer]
    return playerRating


csv_file1 = open('MatchupGenerate.csv', 'r')
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
            HomeAdv[Team2]=0
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
            print(Team1, row1[3], Team2, noOfPredictions, match,"Prediction Rate",noOfPredictions/match)
            playerRating= elo(playerRating, minutesPlayed, Team1, Team2, int(row1[4]), plusminus1, plusminus2)
            '''
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
            TeamRating[Team1] = m1
            TeamRating[Team2] = m2
            print("%%%%%%%%%%%% after update%%%%%%%%%%%%%%%")
            #print("Updated rating for {}".format(Team1), round(p1))
            #print("updated rating for {}".format(Team2), round(p2))
            #print("total2",p1+p2)
            #time.sleep(2)
            #print("Match number", match)
            '''
            '''
            sumTeam1 = 0
            for Teeam in TeamRating:
                sumTeam1 = sumTeam1 + TeamRating[Teeam]
                    # print(Teeam,TeamRating[Teeam])
            print("Total team sum",sumTeam1)
            sumTeam = 0
            for Teeam in minutesPlayed:
                for player in minutesPlayed[Teeam]:
                    sumTeam = sumTeam + playerRating[player]
            print("Sum of team rating2", sumTeam)
            TotalPlayer=0
            for Team in minutesPlayed:
                for player in minutesPlayed[Team]:
                    TotalPlayer+=1
            #print('Total number of players',TotalPlayer)
            '''
            if match == 1230:
                #print(sorted(TeamRating.values()))
                #print(TeamRating)
                sumTeam=0
                for Teeam in TeamRating:
                    sumTeam = sumTeam + TeamRating[Teeam]
    i = i + 1

SUM=sum(avg)    # computing the constant value
#print("average",SUM/number)
csv_file1.close()


