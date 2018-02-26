from collections import defaultdict
import collections
import time
import re
import csv
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
def logistic(x):
    y = 1 / (1 + pow(10, -(x) / 40))
    return (y)
def K(playerRating, minutesPlayed, Team1, Team2, TotTime, plusminus1,plusminus2,x1,x2):
    m1 = 0
    m2 = 0
    NumOfPlayer = 0
    Sum = 0
    K = 30
    Offset = defaultdict(dict)
    for players in plusminus1:
        #print("Minutes Played",minutesPlayed[Team1][players],players)
        m1 += playerRating[players] * minutesPlayed[Team1][players]
    for players in plusminus2:
        m2 += playerRating[players] * minutesPlayed[Team2][players]
    for fixedPlayer in plusminus1:
        new = TotTime - minutesPlayed[Team1][fixedPlayer]
        m1without = ((m1 - playerRating[fixedPlayer] * minutesPlayed[Team1][fixedPlayer]) * TotTime) / new
        minPlayedByPlayer = minutesPlayed[Team1][fixedPlayer]  # *int(TotTime)
        s = playerRating[fixedPlayer] + 4 * m1without - 5 * m2
        if minPlayedByPlayer!=0:
            x1.append(plusminus1[fixedPlayer] / minPlayedByPlayer)
            x2.append(s)
            print("AAAAAAAAAAAAAAA",plusminus1[fixedPlayer] / minPlayedByPlayer,s)
        NumOfPlayer = NumOfPlayer + 1
    # calculating offset for Team2
    for fixedPlayer in plusminus2:
        new = TotTime - minutesPlayed[Team2][fixedPlayer]
        m2without = ((m2 - playerRating[fixedPlayer] * minutesPlayed[Team2][fixedPlayer]) * TotTime) / new
        minPlayedByPlayer = minutesPlayed[Team2][fixedPlayer]  # *int(TotTime)
        s=playerRating[fixedPlayer]+4*m2without-5*m1
        if minPlayedByPlayer!=0:
            x1.append(plusminus2[fixedPlayer]/minPlayedByPlayer)
            x2.append(s)
            print("AAAAAAAAAAAAAAA",plusminus2[fixedPlayer] / minPlayedByPlayer,s)
        NumOfPlayer = NumOfPlayer + 1

    mean = Sum / NumOfPlayer
    # Updating the player ratings
    sum = 0
    offset = 0
    for fixedPlayer in plusminus1:
        Offset[fixedPlayer] = round(Offset[fixedPlayer] - mean)
        playerRating[fixedPlayer] = playerRating[fixedPlayer] + Offset[fixedPlayer]
        offset = Offset[fixedPlayer] + offset
        sum = sum + playerRating[fixedPlayer]
    for fixedPlayer in plusminus2:
        Offset[fixedPlayer] = round(Offset[fixedPlayer] - mean)
        playerRating[fixedPlayer] = playerRating[fixedPlayer] + Offset[fixedPlayer]
        offset = Offset[fixedPlayer] + offset
        sum = sum + playerRating[fixedPlayer]
    print("The sum of the players", sum, NumOfPlayer, sum / NumOfPlayer)
    print("Sum of offsets", offset)
    return x1,x2,playerRating


csv_file1 = open('TeamMatchups.csv', 'r')
reader1 = csv.reader(csv_file1)
i = 0
j = 0
x1=[]
x2=[]
noOfPredictions = 0
minutesPlayed = defaultdict(dict)
playerRating = defaultdict(dict)
plusminus = defaultdict(dict)
duplicate = defaultdict(dict)
tempTeam = defaultdict(dict)
check = defaultdict(dict)
TeamRating = defaultdict(dict)
checklist = []
flog = 1
match = 0
for row1 in reader1:
    plusminus1 = defaultdict(dict)
    plusminus2 = defaultdict(dict)
    if i > 0:
        s = re.split('\W+', row1[2])
        # print(s)
        if len(s) == 2:
            Team1 = s[0]
            Team2 = s[1]
            c = Team1 + Team2
        else:
            Team1 = s[0]
            Team2 = s[2]
            c = Team2 + Team1
        if not (c in checklist):
            csv_file2 = open('PlayerDetails.csv', 'r')
            reader2 = csv.reader(csv_file2)
            for row2 in reader2:
                if j > 0:
                    if (Team1 == row2[1] or Team2 == row2[1]) and row1[1] == row2[2]:
                        # print(row2[0],"playername",row2[1],"team",row2[2],"date")
                        # time.sleep(2)
                        if Team1 == row2[1]:
                            minutesPlayed[Team1][row2[0]] = int(row2[5]) / (int(row1[4]))
                            #print(minutesPlayed[Team1][row2[0]],row2[0])
                            plusminus1[row2[0]] = int(row2[7])
                            if check[row2[0]] == {}:
                                playerRating[row2[0]] = 200
                                check[row2[0]] = 'Filled'
                                #print("enter the dragon")
                                #print(row2[0])
                            #if row2[0]=='Ersan Ilyasova':
                            #    print("PLAYERRRRRRRRRRRRRR",playerRating[row2[0]])
                        elif Team2==row2[1]:
                            minutesPlayed[Team2][row2[0]] = int(row2[5]) / (int(row1[4]))
                            #print(minutesPlayed[Team2][row2[0]], row2[0])
                            plusminus2[row2[0]] = int(row2[7])
                            if check[row2[0]] == {}:
                                playerRating[row2[0]] = 200
                                check[row2[0]] = 'Filled'
                                #print("enter the dragon2")
                                #print(row2[0])
                            #if row2[0]=='Ersan Ilyasova':
                            #    print("PLAYERRRRRRRRRRRRRR",playerRating[row2[0]])
                        else:
                            minutesPlayed[Team1][row2[0]]=0
                            minutesPlayed[Team2][row2[0]]=0

                j = j + 1
            j = 0
            csv_file2.close()
            checklist.append(c)

            # rating update for the 2 teams
            m1 = 0
            m2 = 0
            for players in minutesPlayed[Team1]:
                m1 += playerRating[players] * minutesPlayed[Team1][players]
            for players in minutesPlayed[Team2]:
                m2 += playerRating[players] * minutesPlayed[Team2][players]
            #print("%%%%%%%%%%%%%%%%%  Before Update %%%%%%%%%%%%%%%%")
            #print("Updated rating for {}".format(Team1), round(m1))
            #print("updated rating for {}".format(Team2), round(m2))
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
            #print(Team1, row1[3], Team2, noOfPredictions, match)
            #print("random")
            duplicate = playerRating
            x1,x2, playerRating = K(playerRating, minutesPlayed, Team1, Team2, int(row1[4]), plusminus1, plusminus2,x1,x2)
        else:
            # print("Trying to repeat")
            # time.sleep(10)
            checklist.remove(c)

    # print("NEXT ROUND")
    i = i + 1
print("Lengths of x1 and x2",len(x1),len(x2))
x1=np.array(x1)
x2=np.array(x2)
regr=linear_model.LinearRegression()
regr.fit(x1.reshape(-1,1),x2.reshape(-1,1))
print('Coefficients',regr.coef_)
y_cap=regr.predict(x1.reshape(-1,1))
print("Mean squared error: %.2f"% mean_squared_error(x2, y_cap))
print('Variance score: %.2f' % r2_score(x2, y_cap))
plt.scatter(x1.reshape(-1,1), x2.reshape(-1,1),  color='purple')
#plt.plot(x1.reshape(-1,1),y_cap,color='red')
def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
x=np.linspace(-2000,1500,150)
y=[]
for i in range(0,150):
    y.append(-100*gaussian(x[i],0,300))
y=np.array(y)
plt.plot(x.reshape(-1,1),y.reshape(-1,1),color='red')
plt.show()
csv_file1.close()
csv_file2.close()

