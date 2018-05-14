import pandas
import numpy as np
from collections import defaultdict
import re
from sklearn.metrics import mean_squared_error
import estimation as e

def estimate(gamma, eta):
    #csv_file1 = open('MatchupGenerate.csv', 'r')
    df1=pandas.read_csv('MatchupGenerate.csv')
    df2=pandas.read_csv('playerstats.csv')
    row1=df1.values
    totalGames=np.shape(row1)[0]
    #reader1 = csv.reader(csv_file1)
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
    teamRating=defaultdict(dict)
    match = 0
    avg=[]
    number=0
    flag=0
    MSE=[]
    for i in range(1,17):
        Team="T"+str(i)
        teamRating[Team]=0
        teamRating[Team]=1000

    #print("entered first file")
    for i in range(totalGames):
        plusminus1 = defaultdict(dict)
        plusminus2 = defaultdict(dict)
        #print("MATCH NUMBER:",i)
        matchNumber=row1[i][1]
        s = re.split('\W+', row1[i][0])
        #print(s)
        Team1 ="T"+ s[0]
        Team2 ="T"+ s[3]
        flag=1
        HomeAdv[Team1]=0
        HomeAdv[Team2]=0
        for fixedPlayer in minutesPlayed[Team1]:
            minutesPlayed[Team1][fixedPlayer] = 0
            plusminus1[fixedPlayer]=0
        for fixedPlayer in minutesPlayed[Team2]:
            minutesPlayed[Team2][fixedPlayer] = 0
            plusminus2[fixedPlayer]=0
        #print("opening player stats")
        df3 = df2.loc[df2["matchnumber"] == matchNumber]
        row2=df3.loc[df3["Team"]==Team1].values
        nop=np.shape(row2)[0]
        for j in range(nop):
            minutesPlayed[Team1][row2[j][1]] = float(row2[j][3]) / (float(row1[i][5]))
            plusminus1[row2[j][1]] = float(row2[j][4])
            TrueStrength[row2[j][1]]=float(row2[j][6])
            if check[row2[j][1]] == {}:
                playerRating[row2[j][1]] = 1000
                check[row2[j][1]] = 'Filled'
        df3 = df2.loc[df2["matchnumber"] == matchNumber]
        row2 = df3.loc[df3["Team"] == Team2].values
        nop = np.shape(row2)[0]
        for j in range(nop):
            minutesPlayed[Team2][row2[j][1]] = float(row2[j][3]) / (float(row1[i][6]))
            plusminus2[row2[j][1]] = float(row2[j][4])
            TrueStrength[row2[j][1]] = float(row2[j][6])
            if check[row2[j][1]] == {}:
                playerRating[row2[j][1]] = 1000
                check[row2[j][1]] = 'Filled'

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
        if outcome == row1[i][2]:
            noOfPredictions = noOfPredictions + 1
            W = 1
        else:
            W = 0
        match = match + 1
        #print(Team1, row1[2], Team2, noOfPredictions, match,"Prediction Rate",noOfPredictions/match)
        playerRating= e.eloModified(playerRating, minutesPlayed, Team1, Team2, float(row1[i][5]), float(row1[i][6]), plusminus1, plusminus2,gamma,eta)
        m1 = 0
        m2 = 0
        for players in minutesPlayed[Team1]:
            m1 += playerRating[players] * minutesPlayedEstimate[players]
        for players in minutesPlayed[Team2]:
            m2 += playerRating[players] * minutesPlayedEstimate[players]
        teamRating[Team1]=m1
        teamRating[Team2]=m2
        #teamRating1 = e.playerToTeamRating1(playerRating, minutesPlayedEstimate, minutesPlayedTrue)
        #teamRatingTrue = e.playerToTeamRating(playerRatingTrue, minutesPlayedTrue, minutesPlayedTrue)
        #x1 = e.dictToInt(teamRating)
        #x2 = e.dictToInt(teamRatingTrue)
        #MSE.append(mean_squared_error(x1, x2))
    #print("ESTIMATED WITH THESIS")
    #print("Number of correct predicitons:" ,noOfPredictions,"Total number of games:", match, "Prediction Rate", noOfPredictions / match)
    return playerRating,minutesPlayedEstimate
