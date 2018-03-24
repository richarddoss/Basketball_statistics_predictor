from collections import defaultdict
import collections
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
import random
csv_file1 = open('MatchupGenerate.csv', 'w')
writer1=csv_file1.writer(csv_file1)
writer1.writerow(["Team1 v/s Team2","Game Number","W/L"])
csv_file2=open("playerstats.csv","w")
writer2=csv_file2.writer(csv_file2)
writer2.writerow(["matchnumber","Player Name","Minutes Played","+/-"])
#csv_file2.close()
playerRating=defaultdict(dict)
minutesPlayed=defaultdict(dict)
playerRatingTrue=defaultdict(dict)
minutesPlayedTrue=defaultdict(dict)
PlusMinus=defaultdict(dict)
#initialization of player strengths
for i in range(1,16):
    timePlayed=[random.randint(5, 10) for _ in range(10)]
    sum1=sum(timePlayed)
    timePlayed=(timePlayed/sum1)*240
    for j in range(1,11):
        Team="T"+str(i)
        player="P"+str(j)+Team
        playerRatingTrue[Team][player]=np.random.beta(1.5,3)*3030
        minutesPlayedTrue[Team][player]=timePlayed[j-1]
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
    for fixedPlayer in playerRatingTrue[Team1]:
        playerRating[Team1][fixedPlayer]=np.random.normal(playerRatingTrue[Team1][fixedPlayer],300,1)
        timePlayed[Team1][fixedPlayer]=np.random.normal(minutesPlayedTrue[Team1][fixedPlayer],25,1)
        TotalTime1+=timePlayed[Team1][fixedPlayer]
    for fixedPlayer in playerRatingTrue[Team2]:
        playerRating[Team2][fixedPlayer]=np.random.normal(playerRatingTrue[Team2][fixedPlayer],300,1)
        timePlayed[Team2][fixedPlayer]=np.random.normal(minutesPlayedTrue[Team2][fixedPlayer],25,1)
        TotalTime2+=timePlayed[Team1][fixedPlayer]
    m1=0
    m2=0
    for fixedPlayer in playerRatingTrue[Team1]:
        m1+=playerRating[Team1][fixedPlayer]*minutesPlayed[Team1][fixedPlayer]
    for fixedPlayer in playerRatingTrue[Team2]:
        m2+=playerRating[Team2][fixedPlayer]*minutesPlayed[Team2][fixedPlayer]
    for fixedPlayer in playerRating[Team1]:
        minutesPlayedbyPlayer=minutesPlayed[Team1][fixedPlayer]
        m1without=(m1-timePlayed[Team1][fixedPlayer]*playerRating[Team1][fixedPlayer])/(TotalTime1-minutesPlayedbyPlayer)
        PlusMinus[Team1][fixedPlayer]=((playerRating[Team1][fixedPlayer]+4*m1without-5*m2)*minutesPlayedbyPlayer)/2500
        writer2.writerow([str(i),fixedPlayer,minutesPlayedbyPlayer,PlusMinus[Team1][fixedPlayer]])
    for fixedPlayer in playerRating[Team2]:
        minutesPlayedbyPlayer=minutesPlayed[Team2][fixedPlayer]
        m1without=(m1-timePlayed[Team2][fixedPlayer]*playerRating[Team2][fixedPlayer])/(TotalTime1-minutesPlayedbyPlayer)
        PlusMinus[Team2][fixedPlayer]=((playerRating[Team2][fixedPlayer]+4*m1without-5*m2)*minutesPlayedbyPlayer)/2500
        writer2.writerow([str(i), fixedPlayer, minutesPlayedbyPlayer, PlusMinus[Team2][fixedPlayer]])
    PTS1=m1*TotalTime1
    PTS2=m2*TotalTime2
    if PTS1>PTS2:
        column3="W"
    else:
        column3="L"
    writer1.writerow([column1,column2,column3])
csv_file1.close()
csv_file2.close()




