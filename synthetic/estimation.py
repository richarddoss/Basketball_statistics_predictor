from collections import defaultdict
import collections
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np


def logistic(x):
    y = (1 / (1 + pow(10, -(x) / 40)))-0.5
    return (y)

def eloModified(playerRating, minutesPlayed, Team1, Team2, TotTime1, TotTime2, plusminus1,plusminus2,K):
    m1 = 0
    m2 = 0
    NumOfPlayer = 0
    Sum = 0
    #K = 500
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
        new = TotTime1 - minutesPlayed[Team1][fixedPlayer]*TotTime1
        m1without = ((m1 - playerRating[fixedPlayer] * minutesPlayed[Team1][fixedPlayer]) * TotTime1) / new
        minPlayedByPlayer = minutesPlayed[Team1][fixedPlayer]  # *int(TotTime)
        PtTeam = minPlayedByPlayer * playerRating[fixedPlayer] + 4 * minPlayedByPlayer * m1without
        PtOppTeam = minPlayedByPlayer * 5 * m2
        X = round(PtTeam - PtOppTeam)
        X=X*(TotTime1/2500)
        PtDiff=plusminus1[fixedPlayer]-X
        Offset[fixedPlayer] = K * (round(logistic(PtDiff),2))
        Sum = Sum + 5*minPlayedByPlayer*Offset[fixedPlayer]
        NumOfPlayer = NumOfPlayer + 1
        w1+=5*minPlayedByPlayer
    # calculating offset for Team2
    for fixedPlayer in minutesPlayed[Team2]:
        new = TotTime2 - minutesPlayed[Team2][fixedPlayer]
        m2without = ((m2 - playerRating[fixedPlayer] * minutesPlayed[Team2][fixedPlayer]) * TotTime2) / new
        minPlayedByPlayer = minutesPlayed[Team2][fixedPlayer]  # *int(TotTime)
        PtTeam = minPlayedByPlayer * playerRating[fixedPlayer] + 4 * minPlayedByPlayer * m2without
        PtOppTeam = minPlayedByPlayer * 5 * m1
        X = round(PtTeam - PtOppTeam)
        X = X * (TotTime2 / 2500)
        PtDiff = plusminus2[fixedPlayer] - X
        Offset[fixedPlayer] = K * (round(logistic(PtDiff), 2))
        Sum = Sum + 5*minPlayedByPlayer*Offset[fixedPlayer]
        NumOfPlayer = NumOfPlayer + 1
        w2+=5*minPlayedByPlayer
    # Updating the player ratings
    #print("next phase")
    sum=0
    offset=0
    for fixedPlayer in minutesPlayed[Team1]:
        Offset[fixedPlayer]=5*minutesPlayed[Team1][fixedPlayer]*(2*Offset[fixedPlayer]-Sum/w1)
        playerRating[fixedPlayer] = playerRating[fixedPlayer] + Offset[fixedPlayer]
        offset=Offset[fixedPlayer]+offset
        sum=sum+playerRating[fixedPlayer]
    for fixedPlayer in minutesPlayed[Team2]:
        Offset[fixedPlayer] = 5*minutesPlayed[Team2][fixedPlayer] * (2 * Offset[fixedPlayer] - Sum/w2)
        playerRating[fixedPlayer] = playerRating[fixedPlayer] + Offset[fixedPlayer]
        offset = Offset[fixedPlayer] + offset
        sum=sum+playerRating[fixedPlayer]
    return playerRating

def estimate(K):
    csv_file1 = open('MatchupGenerate.csv', 'r')
    reader1 = csv.reader(csv_file1)
    i = 0
    j = 0
    noOfPredictions = 0
    minutesPlayed = defaultdict(dict)
    minutesPlayedEstimate = defaultdict(dict)
    NumberMinutes=defaultdict(dict)
    playerRating = defaultdict(dict)
    check = defaultdict(dict)
    TeamRating = defaultdict(dict)
    HomeAdv = defaultdict(dict)
    TrueStrength= defaultdict(dict)
    match = 0
    avg=[]
    number=0
    flag=0
    print("entered first file")
    for row1 in reader1:
        plusminus1 = defaultdict(dict)
        plusminus2 = defaultdict(dict)
        if i > 0:
            #print("MATCH NUMBER:",i)
            matchNumber=row1[1]
            s = re.split('\W+', row1[0])
            #print(s)
            Team1 ="T"+ s[0]
            Team2 ="T"+ s[3]
            flag=1
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
                #print("opening player stats")
                csv_file2 = open('playerstats.csv', 'r')
                print("opened second file")
                reader2 = csv.reader(csv_file2)
                for row2 in reader2:
                    if j > 0:
                        if matchNumber==row2[0]:
                            if Team1 == row2[2]:
                                minutesPlayed[Team1][row2[1]] = float(row2[3]) / (float(row1[5]))
                                plusminus1[row2[1]] = float(row2[4])
                                TrueStrength[row2[1]]=float(row2[6])
                                if check[row2[1]] == {}:
                                    playerRating[row2[1]] = 1000
                                    check[row2[1]] = 'Filled'
                            elif Team2==row2[2]:
                                minutesPlayed[Team2][row2[1]] = float(row2[3]) / (float(row1[6]))
                                plusminus2[row2[1]] = float(row2[4])
                                TrueStrength[row2[1]] = float(row2[6])
                                if check[row2[1]] == {}:
                                    playerRating[row2[1]] = 1000
                                    check[row2[1]] = 'Filled'
                    j = j + 1
                j = 0
                csv_file2.close()
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
                for players in minutesPlayed[Team1]:
                    m1 += playerRating[players] * minutesPlayedEstimate[players]
                for players in minutesPlayed[Team2]:
                    m2 += playerRating[players] * minutesPlayedEstimate[players]
                m1+=HomeAdv[Team1]
                m2 += HomeAdv[Team2]
                if m1 > m2:
                    outcome = 'W'
                else:
                    outcome = 'L'
                if outcome == row1[2]:
                    noOfPredictions = noOfPredictions + 1
                    W = 1
                else:
                    W = 0
                match = match + 1
                #print(Team1, row1[2], Team2, noOfPredictions, match,"Prediction Rate",noOfPredictions/match)
                playerRating= eloModified(playerRating, minutesPlayed, Team1, Team2, float(row1[5]), float(row1[6]), plusminus1, plusminus2,K)
        i = i + 1
    csv_file1.close()
    print("ESTIMATED WITH THESIS")
    print("Number of correct predicitons:" ,noOfPredictions,"Total number of games:", match, "Prediction Rate", noOfPredictions / match)
    return playerRating,minutesPlayedEstimate,noOfPredictions

def store(playerRating,TrueStrength):
    csv_file3= open("cross.csv",'w')
    writer3=csv.writer(csv_file3)
    writer3.writerow(["Player Name","Estimated Strength","True Strength"])
    for player in playerRating:
        writer3.writerow([player,playerRating[player],TrueStrength[player]])

def MeanSquareError(playerRating,TrueStrength):
    MSE=0
    sum=0
    number=0
    for player in playerRating:
        MSE+=pow(playerRating[player]-TrueStrength[player],2)
        sum+=playerRating[player]
        number+=1
    #print(sum,number)
    time.sleep(5)
    return(MSE)
def dictToInt(playerStrength):
    player=np.zeros(160)
    k=0
    for p in playerStrength:
        player[k]=playerStrength[p]
        k+=1
    return(player)
def playerToTeamRating(players,time,timeTrue):
    teamRating=defaultdict(dict)
    for i in range(1,17):
        Team="T"+str(i)
        teamRating[Team]=0
        for player in timeTrue[Team]:
            #print(player,time[player],players[player])
            teamRating[Team]+= players[Team][player]* time[Team][player]
        teamRating[Team]=teamRating[Team]/240
    return(teamRating)

def playerToTeamRating1(players,time,timeTrue):
    teamRating=defaultdict(dict)
    for i in range(1,17):
        Team="T"+str(i)
        teamRating[Team]=0
        for player in timeTrue[Team]:
            #print(player,time[player],players[player])
            teamRating[Team]+= players[player]* time[player]
        teamRating[Team]=teamRating[Team]
    return(teamRating)





