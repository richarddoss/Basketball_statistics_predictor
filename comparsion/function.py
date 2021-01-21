from collections import defaultdict
import collections
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np

# logistic function as defined for elo
def logistic(x):
    y = (1 / (1 + pow(10, -(x) / 40)))-0.5
    return (y)

# Modified Elo code that uses the +/- score to update player rating
def elo(playerRating, minutesPlayed, Team1, Team2, TotTime, plusminus1,plusminus2,K,N):
    m1 = 0
    m2 = 0
    NumOfPlayer = 0
    Sum = 0
    #K = 150
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
        X=X*(TotTime/N)
        PtDiff=plusminus1[fixedPlayer]-X
        Offset[fixedPlayer] = K * (round(logistic(PtDiff),2))
        Sum = Sum + 5*minPlayedByPlayer*Offset[fixedPlayer]
        NumOfPlayer = NumOfPlayer + 1
        w1+=(5*minPlayedByPlayer)

    # calculating offset for Team2
    for fixedPlayer in minutesPlayed[Team2]:
        new = TotTime - minutesPlayed[Team2][fixedPlayer]
        m2without = ((m2 - playerRating[fixedPlayer] * minutesPlayed[Team2][fixedPlayer]) * TotTime) / new
        minPlayedByPlayer = minutesPlayed[Team2][fixedPlayer]  # *int(TotTime)
        PtTeam = minPlayedByPlayer * playerRating[fixedPlayer] + 4 * minPlayedByPlayer * m2without
        PtOppTeam = minPlayedByPlayer * 5 * m1
        X = round(PtTeam - PtOppTeam)
        X = X * (TotTime /N)
        PtDiff = plusminus2[fixedPlayer] - X
        Offset[fixedPlayer] = K * (round(logistic(PtDiff), 2))
        Sum = Sum + 5*minPlayedByPlayer*Offset[fixedPlayer]
        NumOfPlayer = NumOfPlayer + 1
        w2+=(5*minPlayedByPlayer)

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
