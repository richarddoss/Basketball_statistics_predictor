from collections import defaultdict
import collections
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
import random
csv_file1 = open('MatchupGenerate.csv', 'w')
writer1=csv.writer(csv_file1)
writer1.writerow(["Team1 v/s Team2","Game Number","W/L","Team1 strength","Team2 strength","Total Time 1","Total Time 2"])
csv_file2=open("playerstats.csv","w")
writer2=csv.writer(csv_file2)
writer2.writerow(["matchnumber","Player Name","Minutes Played","+/-","Player strength","True Player Strength"])
#csv_file2.close()
playerRating=defaultdict(dict)
minutesPlayed=defaultdict(dict)
playerRatingTrue=defaultdict(dict)
minutesPlayedTrue=defaultdict(dict)
PlusMinus=defaultdict(dict)
timePlayed=defaultdict(dict)
#initialization of player strengths
for i in range(1,16):
    timePlayedint=[random.randint(5, 10) for _ in range(10)]
    sum1=sum(timePlayedint)
    timePlayedint=(np.divide(timePlayedint,sum1))*240
    for j in range(1,11):
        Team="T"+str(i)
        player="P"+str(j)+Team
        playerRatingTrue[Team][player]=round((np.random.beta(1.5,5)*600)+900)
        minutesPlayedTrue[Team][player]=timePlayedint[j-1]
#matchup Generation
for i in range(0,10):
    [T1,T2]=random.sample(range(1,15),2)
    Team1="T"+str(T1)
    Team2="T"+str(T2)
    column1=str(T1)+" v/s "+str(T2)
    column2=i
    #csv_file2 = open("playerstats.csv", "a")
    #writer2 = csv_file2.writer(csv_file2)
    TotalTime1=0
    TotalTime2=0
    timePlayedT1 = [random.randint(5, 10) for _ in range(10)]
    sum1 = sum(timePlayedT1)
    timePlayedT1 = (np.divide(timePlayedT1, sum1)) * 240
    timePlayedT2 = [random.randint(5, 10) for _ in range(10)]
    sum1 = sum(timePlayedT2)
    timePlayedT2 = (np.divide(timePlayedT2, sum1)) * 240
    k=0
    for fixedPlayer in playerRatingTrue[Team1]:
        playerRating[Team1][fixedPlayer]=np.random.normal(playerRatingTrue[Team1][fixedPlayer],100)
        #minutesPlayed[Team1][fixedPlayer]=np.random.normal(minutesPlayedTrue[Team1][fixedPlayer],25)
        minutesPlayed[Team1][fixedPlayer]=round(timePlayedT1[k])
        k+=1
        print(minutesPlayed[Team1][fixedPlayer],playerRating[Team1][fixedPlayer], Team1, fixedPlayer)
        TotalTime1+=minutesPlayed[Team1][fixedPlayer]
    print("TotalTime 1",TotalTime1)
    k=0
    for fixedPlayer in playerRatingTrue[Team2]:
        playerRating[Team2][fixedPlayer]=np.random.normal(playerRatingTrue[Team2][fixedPlayer],300)
        #minutesPlayed[Team2][fixedPlayer]=np.random.normal(minutesPlayedTrue[Team2][fixedPlayer],25)
        minutesPlayed[Team2][fixedPlayer]=round(timePlayedT2[k])
        k+=1
        print(minutesPlayed[Team2][fixedPlayer], playerRating[Team2][fixedPlayer], Team2, fixedPlayer)
        TotalTime2+=minutesPlayed[Team2][fixedPlayer]
    print("Total TIme 2",TotalTime2)
    m1=0
    m2=0
    for fixedPlayer in playerRatingTrue[Team1]:
        m1+=playerRating[Team1][fixedPlayer]*minutesPlayed[Team1][fixedPlayer]
    m1=m1/TotalTime1
    print("Team 1 effective strength",m1)
    #time.sleep(2)
    for fixedPlayer in playerRatingTrue[Team2]:
        m2+=playerRating[Team2][fixedPlayer]*minutesPlayed[Team2][fixedPlayer]
    m2=m2/TotalTime2
    print('Team2 effective strength',m2)
    #time.sleep(2)
    for fixedPlayer in playerRating[Team1]:
        minutesPlayedbyPlayer=minutesPlayed[Team1][fixedPlayer]
        m1without=((m1*TotalTime1)-(minutesPlayed[Team1][fixedPlayer]*playerRating[Team1][fixedPlayer]))/(TotalTime1-minutesPlayedbyPlayer)
        print("m1 without",m1without)
        #time.sleep(2)
        PlusMinus[Team1][fixedPlayer]=((playerRating[Team1][fixedPlayer]+4*m1without-5*m2)*minutesPlayedbyPlayer)/2500
        print("plusminus",PlusMinus[Team1][fixedPlayer])
        writer2.writerow([str(i),fixedPlayer,minutesPlayedbyPlayer,PlusMinus[Team1][fixedPlayer],playerRating[Team1][fixedPlayer],playerRatingTrue[Team1][fixedPlayer]])
    for fixedPlayer in playerRating[Team2]:
        minutesPlayedbyPlayer=minutesPlayed[Team2][fixedPlayer]
        m2without=((m2*TotalTime2)-minutesPlayed[Team2][fixedPlayer]*playerRating[Team2][fixedPlayer])/(TotalTime1-minutesPlayedbyPlayer)
        print("m2 without", m2without)
        #time.sleep(2)
        PlusMinus[Team2][fixedPlayer]=((playerRating[Team2][fixedPlayer]+4*m2without-5*m1)*minutesPlayedbyPlayer)/2500
        print("plusminus", PlusMinus[Team2][fixedPlayer])
        writer2.writerow([str(i), fixedPlayer, minutesPlayedbyPlayer, PlusMinus[Team2][fixedPlayer],playerRating[Team2][fixedPlayer],playerRatingTrue[Team2][fixedPlayer]])
    PTS1=m1*TotalTime1
    PTS2=m2*TotalTime2
    if PTS1>PTS2:
        column3="W"
    else:
        column3="L"
    column4=m1
    column5=m2
    column6=TotalTime1
    column7=TotalTime2
    writer1.writerow([column1,column2,column3,column4,column5,column6,column7])
csv_file1.close()
csv_file2.close()




