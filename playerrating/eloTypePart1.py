from collections import defaultdict
import collections
import time
import re
import csv
def logistic(x):
	y=1/(1+pow(10,-(x)))
	return(y)
def elo(fixedPlayer,playerRating,minutesPlayed,Team,OppTeam,TotTime,PTS):
	m1=0
	m2=0
	print("Pre-Update player Rating for {} is".format(fixedPlayer),playerRating[Team][fixedPlayer],"TEAM:{}".format(Team))
	for players in playerRating[Team]:
		m1+=playerRating[Team][players]*minutesPlayed[Team][players]
	for players in playerRating[OppTeam]:
		m2+=playerRating[OppTeam][players]*minutesPlayed[OppTeam][players]
	new=TotTime-minutesPlayed[Team][fixedPlayer]
	m1without=((m1-playerRating[Team][fixedPlayer]*minutesPlayed[Team][fixedPlayer])*Totime)/new
	#print("effective strength for {} player's team".format(fixedPlayer),m1without,"Effective strength for opp team",m2)
	minPlayedByPlayer=minutesPlayed[Team][fixedPlayer]*int(TotTime)
	minWithPlayer=int(TotTime)-minWithoutPlayer
	PtTeam=minPlayedByPlayer*playerRating[Team][fixedPlayer]+4*minPlayedByPlayer*m1without
	PtOppTeam=minPlayedByPlayer*5*m2
	#print("PointProduction by {}".format(Team),PtTeam)
	#print("PointProduction by {}".format(OppTeam),PtOppTeam)
	expectedValue=PtTeam-PtOppTeam
	#print("Actual",PTS,"Expected",expectedValue)
	updateValue=(10*(PTS-expectedValue))/int(TotTime)
	playerRating[Team][fixedPlayer]=playerRating[Team][fixedPlayer]+updateValue
	print("Updated player Rating for {} is".format(fixedPlayer),playerRating[Team][fixedPlayer],"TEAM:{}".format(Team))
	#time.sleep(10)
	return playerRating
	
csv_file1 = open('TeamMatchups.csv', 'r')
reader1 = csv.reader(csv_file1)
i=0
j=0
minutesPlayed=defaultdict(dict)
playerRating=defaultdict(dict)
duplicate=defaultdict(dict)
tempTeam=defaultdict(dict)
check=defaultdict(dict)
checklist=[]
flog=1
for row1 in reader1:
	if i>0:
		s=re.split('\W+',row1[2])
		#print(s)
		if len(s)==2:
			Team1=s[0]
			Team2=s[1]
			c=Team1+Team2
		else:
			Team1=s[0]
			Team2=s[2]
			c=Team2+Team1
		if not(c in checklist):
			csv_file2 = open('PlayerDetails.csv', 'r')
			reader2 = csv.reader(csv_file2)
			for row2 in reader2:
				if j>0:
					if (Team1==row2[1] or Team2==row2[1]) and row1[1]==row2[2]:
						#print(row2[0],"playername",row2[1],"team",row2[2],"date")
						#time.sleep(2)
						if Team1==row2[1]:
							minutesPlayed[Team1][row2[0]]=int(row2[5])/(int(row1[4]))
							if check[row2[0]]=={}:
								playerRating[Team1][row2[0]]=200
								check[row2[0]]='Filled'
								print("enter the dragon")
						else:
							minutesPlayed[Team2][row2[0]]=int(row2[5])/(int(row1[4]))
							if check[row2[0]]=={}:
								playerRating[Team2][row2[0]]=200
								check[row2[0]]='Filled'
								print("enter the dragon2")
				j=j+1
			j=0
			csv_file2.close()
			checklist.append(c)
			print("%%%%%%%%%%%%%%%%%  Before Update %%%%%%%%%%%%%%%%")
			m1=0
			m2=0
			for players in playerRating[Team1]:
				m1+=playerRating[Team1][players]*minutesPlayed[Team1][players]
			for players in playerRating[Team2]:
				m2+=playerRating[Team2][players]*minutesPlayed[Team2][players]
			print("Updated rating for {}".format(Team1),m1)
			print("updated rating for {}".format(Team2),m2)
			print(Team1,row1[3],Team2)
			print("%%%%%%%%%%%% after update%%%%%%%%%%%%%%%")
			duplicate=playerRating
			for fixedPlayer in playerRating[Team1]:
				playerRating=elo(fixedPlayer,playerRating,minutesPlayed,Team1,Team2,row1[4],int(row1[6]))
			tempTeam=playerRating[Team1]
			for fixedPlayer in playerRating[Team2]:
				playerRating=elo(fixedPlayer,duplicate,minutesPlayed,Team2,Team1,row1[4],-1*int(row1[6]))
			playerRating[Team1]=tempTeam
			m1=0
			m2=0
			for players in playerRating[Team1]:
				m1+=playerRating[Team1][players]*minutesPlayed[Team1][players]
			for players in playerRating[Team2]:
				m2+=playerRating[Team2][players]*minutesPlayed[Team2][players]
			print("Updated rating for {}".format(Team1),m1)
			print("updated rating for {}".format(Team2),m2)
			time.sleep(4)
		else:
			print("Trying to repeat")
			#time.sleep(10)
			checklist.remove(c)
		
	print("NEXT ROUND")
	i=i+1
csv_file1.close()
csv_file2.close()
	
