from collections import defaultdict
import collections
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
import random

def generateTrueStrength():
    playerRatingTrue = defaultdict(dict)
    minutesPlayedTrue = defaultdict(dict)
    TotalTime = defaultdict(dict)
    #print("hello")
    for i in range(1, 17):
        Team = "T" + str(i)
        TotalTime[Team]=0
        for j in range(1, 11):
            player = "P" + str(j) + Team
            seed = np.random.beta(1.5, 5)
            playerRatingTrue[Team][player] = round((seed * 600) + 900)
            minutesPlayedTrue[Team][player] = round(seed * 24 + 12)
            TotalTime[Team]+=minutesPlayedTrue[Team][player]
        for k in range(1,11):
            player = "P" + str(k) + Team
            minutesPlayedTrue[Team][player]=(minutesPlayedTrue[Team][player]/TotalTime[Team])*240
    print("TRUE STRENGTH GENERATED")
    return playerRatingTrue,minutesPlayedTrue

def generateTrueTeamStrength():
    teamRatingTrue = defaultdict(dict)
    for i in range(1, 17):
        Team = "T" + str(i)
        seed = np.random.beta(1.5, 5)
        teamRatingTrue[Team] = round((seed * 600) + 900)
    print("TRUE Team STRENGTH GENERATED")
    return teamRatingTrue


def statsGenerate(playerRatingTrue,minutesPlayedTrue,matches):
    csv_file1 = open('MatchupGenerate.csv', 'w')
    writer1=csv.writer(csv_file1)
    writer1.writerow(["Team1 v/s Team2","Game Number","W/L","Team1 strength","Team2 strength","Total Time 1","Total Time 2"])
    csv_file2=open("playerstats.csv","w")
    writer2=csv.writer(csv_file2)
    writer2.writerow(["matchnumber","Player Name","Team","Minutes Played","+/-","Player strength","True Player Strength"])
    csv_file3 = open('Teamstrength.csv', 'w')
    writer3=csv.writer(csv_file3)
    writer3.writerow(["Team","Team strength"])
    csv_file4 = open('playerstrength.csv', 'w')
    writer4=csv.writer(csv_file4)
    writer4.writerow(["Player name","Player strength","True Time played"])
    playerRating=defaultdict(dict)
    minutesPlayed=defaultdict(dict)
    PlusMinus=defaultdict(dict)
    #matchup Generation
    for i in range(0,matches):
        [T1,T2]=random.sample(range(1,17),2)
        Team1="T"+str(T1)
        Team2="T"+str(T2)
        column1=str(T1)+" v/s "+str(T2)
        column2=i
        TotalTime1=0
        TotalTime2=0
        for fixedPlayer in playerRatingTrue[Team1]:
            playerRating[Team1][fixedPlayer]=np.random.normal(playerRatingTrue[Team1][fixedPlayer],100)
            minutesPlayed[Team1][fixedPlayer]=np.random.beta(11.02,11.02)*48
            TotalTime1+=minutesPlayed[Team1][fixedPlayer]
        #print("TotalTime 1",TotalTime1)
        for fixedPlayer in playerRatingTrue[Team2]:
            playerRating[Team2][fixedPlayer]=np.random.normal(playerRatingTrue[Team2][fixedPlayer],300)
            minutesPlayed[Team2][fixedPlayer]=np.random.normal(minutesPlayedTrue[Team2][fixedPlayer],12)
            TotalTime2+=minutesPlayed[Team2][fixedPlayer]
        #print("Total TIme 2",TotalTime2)
        T1=0
        T2=0
        for fixedPlayer in playerRatingTrue[Team1]:
            minutesPlayed[Team1][fixedPlayer]=(minutesPlayed[Team1][fixedPlayer]/TotalTime1)*240
            T1+=minutesPlayed[Team1][fixedPlayer]
        for fixedPlayer in playerRatingTrue[Team2]:
            minutesPlayed[Team2][fixedPlayer]=(minutesPlayed[Team2][fixedPlayer]/TotalTime2)*240
            T2+=minutesPlayed[Team2][fixedPlayer]
        m1=0
        m2=0
        for fixedPlayer in playerRatingTrue[Team1]:
            m1+=playerRating[Team1][fixedPlayer]*minutesPlayed[Team1][fixedPlayer]
        m1=m1/T1
        #print("Team 1 effective strength",m1)
        for fixedPlayer in playerRatingTrue[Team2]:
            m2+=playerRating[Team2][fixedPlayer]*minutesPlayed[Team2][fixedPlayer]
        m2=m2/T2
        #print('Team2 effective strength',m2)
        for fixedPlayer in playerRating[Team1]:
            minutesPlayedbyPlayer=minutesPlayed[Team1][fixedPlayer]
            m1without=((m1*T1)-(minutesPlayed[Team1][fixedPlayer]*playerRating[Team1][fixedPlayer]))/(T1-minutesPlayedbyPlayer)
            #print("m1 without",m1without)
            PlusMinus[Team1][fixedPlayer]=((playerRating[Team1][fixedPlayer]+4*m1without-5*m2)*minutesPlayedbyPlayer)/2500
            #print("plusminus",PlusMinus[Team1][fixedPlayer])
            writer2.writerow([str(i),fixedPlayer,Team1,minutesPlayedbyPlayer,PlusMinus[Team1][fixedPlayer],playerRating[Team1][fixedPlayer],playerRatingTrue[Team1][fixedPlayer]])
        for fixedPlayer in playerRating[Team2]:
            minutesPlayedbyPlayer=minutesPlayed[Team2][fixedPlayer]
            m2without=((m2*T2)-minutesPlayed[Team2][fixedPlayer]*playerRating[Team2][fixedPlayer])/(T2-minutesPlayedbyPlayer)
            #print("m2 without", m2without)
            PlusMinus[Team2][fixedPlayer]=((playerRating[Team2][fixedPlayer]+4*m2without-5*m1)*minutesPlayedbyPlayer)/2500
            #print("plusminus", PlusMinus[Team2][fixedPlayer])
            writer2.writerow([str(i), fixedPlayer, Team2, minutesPlayedbyPlayer, PlusMinus[Team2][fixedPlayer],playerRating[Team2][fixedPlayer],playerRatingTrue[Team2][fixedPlayer]])
        PTS1=m1*T1
        PTS2=m2*T2
        if PTS1>PTS2:
            column3="W"
        else:
            column3="L"
        column4=m1
        column5=m2
        column6=T1
        column7=T2
        writer1.writerow([column1,column2,column3,column4,column5,column6,column7])
    csv_file1.close()
    csv_file2.close()
    for Team in playerRatingTrue:
        m2=0
        for player in playerRatingTrue[Team]:
            m2 += playerRatingTrue[Team][player] * minutesPlayedTrue[Team][player]
            writer4.writerow([player,playerRatingTrue[Team][player],minutesPlayedTrue[Team][player]])
        m2+=m2/240
        writer3.writerow([Team, m2])
    csv_file3.close()
    csv_file4.close()
    print("STATS GENERATED")
    return(playerRating,minutesPlayed)





