from collections import defaultdict
import collections
import time
import re
import csv
def logistic(x):
	y=1/(1+pow(10,-(x)/40))
	return(y)
def elo(playerRating,minutesPlayed,Team1,Team2,TotTime,plusminus):
	m1=0
	m2=0
	NumOfPlayer=0
	Sum=0
	K=60
	Offset=defaultdict(dict)
	actualValue=defaultdict(dict)
	expectedValue=defaultdict(dict)
	#print("Pre-Update player Rating for {} is".format(fixedPlayer),playerRating[Team][fixedPlayer],"TEAM:{}".format(Team))
	for players in playerRating[Team1]:
		m1+=playerRating[Team1][players]*minutesPlayed[Team1][players]
	for players in playerRating[Team2]:
		m2+=playerRating[Team2][players]*minutesPlayed[Team2][players]
	for fixedPlayer in playerRating[Team1]:
		new=TotTime-minutesPlayed[Team1][fixedPlayer]
		m1without=((m1-playerRating[Team1][fixedPlayer]*minutesPlayed[Team1][fixedPlayer])*TotTime)/new
		#print("effective strength for {} player's team".format(fixedPlayer),m1without,"Effective strength for opp team",m2)
		minPlayedByPlayer=minutesPlayed[Team1][fixedPlayer]#*int(TotTime)
		#minWithPlayer=int(TotTime)-minWithoutPlayer
		PtTeam=minPlayedByPlayer*playerRating[Team1][fixedPlayer]+4*minPlayedByPlayer*m1without
		PtOppTeam=minPlayedByPlayer*5*m2
		#print("PointProduction by {}".format(Team1),PtTeam)
		#print("PointProduction by {}".format(Team2),PtOppTeam)
		X=round(PtTeam-PtOppTeam)
		expectedValue[fixedPlayer]=round(logistic(X),2)
		#time.sleep(2)
		actualValue[fixedPlayer]=round(logistic(plusminus[fixedPlayer]),2)
		#print("Logistic value of X",round(expectedValue[fixedPlayer],2),round(actualValue[fixedPlayer],2))
		#print("expected",expectedValue[fixedPlayer],"actualValue",actualValue[fixedPlayer])
		Offset[fixedPlayer]=K*(actualValue[fixedPlayer]-expectedValue[fixedPlayer])
		#print("offset", Offset[fixedPlayer])
		Sum=Sum+Offset[fixedPlayer]
		NumOfPlayer=NumOfPlayer+1
		#calculating offset for Team2
	for fixedPlayer in playerRating[Team2]:
		new=TotTime-minutesPlayed[Team2][fixedPlayer]
		m2without=((m2-playerRating[Team2][fixedPlayer]*minutesPlayed[Team2][fixedPlayer])*TotTime)/new
		#print("effective strength for {} player's team".format(fixedPlayer),m1without,"Effective strength for opp team",m2)
		minPlayedByPlayer=minutesPlayed[Team2][fixedPlayer]#*int(TotTime)
		#minWithPlayer=int(TotTime)-minWithoutPlayer
		PtTeam=minPlayedByPlayer*playerRating[Team2][fixedPlayer]+4*minPlayedByPlayer*m2without
		PtOppTeam=minPlayedByPlayer*5*m1
		#print("PointProduction by {}".format(Team1),PtTeam)
		#print("PointProduction by {}".format(Team2),PtOppTeam)
		X=round(PtTeam-PtOppTeam)
		#print(X)
		expectedValue[fixedPlayer]=round(logistic(X),2)
		#time.sleep(2)
		actualValue[fixedPlayer]=round(logistic(plusminus[fixedPlayer]),2)
		#print("expected",expectedValue[fixedPlayer],"actualValue",actualValue[fixedPlayer])
		#print("Logistic value of X",round(expectedValue[fixedPlayer],2),"actual",round(actualValue[fixedPlayer],2))
		Offset[fixedPlayer]=K*(actualValue[fixedPlayer]-expectedValue[fixedPlayer])
		#print("offset",Offset[fixedPlayer])
		Sum=Sum+Offset[fixedPlayer]
		NumOfPlayer=NumOfPlayer+1

	mean=Sum/NumOfPlayer
	#print("Mean",mean)
	#Updating the player ratings
	for fixedPlayer in playerRating[Team1]:
		#print("Offset",Offset[fixedPlayer],"actualValue",actualValue[fixedPlayer],"expectedValue",expectedValue[fixedPlayer])
		Offset[fixedPlayer]=round(Offset[fixedPlayer]-mean)
		#print("Offset for player",fixedPlayer,Offset[fixedPlayer])
		#time.sleep(2)
		playerRating[Team1][fixedPlayer]=playerRating[Team1][fixedPlayer]+Offset[fixedPlayer]
		#print("Updated player Rating for {} is".format(fixedPlayer),playerRating[Team1][fixedPlayer],"TEAM:{}".format(Team1))
	for fixedPlayer in playerRating[Team2]:
		#print("Offset",Offset[fixedPlayer],"actualValue",actualValue[fixedPlayer],"expectedValue",expectedValue[fixedPlayer])
		Offset[fixedPlayer]=round(Offset[fixedPlayer]-mean)
		#print("Offset for player",fixedPlayer,Offset[fixedPlayer])
		#time.sleep(2)
		playerRating[Team2][fixedPlayer]=playerRating[Team2][fixedPlayer]+Offset[fixedPlayer]
		#print("Updated player Rating for {} is".format(fixedPlayer),playerRating[Team2][fixedPlayer],"TEAM:{}".format(Team2))
	#time.sleep(4)
	return playerRating
	
csv_file1 = open('TeamMatchups.csv', 'r')
reader1 = csv.reader(csv_file1)
i=0
j=0
noOfPredictions=0
minutesPlayed=defaultdict(dict)
playerRating=defaultdict(dict)
plusminus=defaultdict(dict)
duplicate=defaultdict(dict)
tempTeam=defaultdict(dict)
check=defaultdict(dict)
TeamRating=defaultdict(dict)
checklist=[]
flog=1
match=0
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
							plusminus[row2[0]]=int(row2[7])
							if check[row2[0]]=={}:
								playerRating[Team1][row2[0]]=200
								check[row2[0]]='Filled'
								#print("enter the dragon")
						else:
							minutesPlayed[Team2][row2[0]]=int(row2[5])/(int(row1[4]))
							plusminus[row2[0]]=int(row2[7])
							if check[row2[0]]=={}:
								playerRating[Team2][row2[0]]=200
								check[row2[0]]='Filled'
								#print("enter the dragon2")
				j=j+1
			j=0
			csv_file2.close()
			checklist.append(c)
			
			#rating update for the 2 teams
			m1=0
			m2=0
			for players in playerRating[Team1]:
				m1+=playerRating[Team1][players]*minutesPlayed[Team1][players]
			for players in playerRating[Team2]:
				m2+=playerRating[Team2][players]*minutesPlayed[Team2][players]
			if Team1=='LAC' or Team2=='LAC':
				print("%%%%%%%%%%%%%%%%%  Before Update %%%%%%%%%%%%%%%%")
				print("Updated rating for {}".format(Team1),round(m1))
				print("updated rating for {}".format(Team2),round(m2))
			if m1>m2:
				outcome='W'
			else:
				outcome='L'
			if outcome==row1[3]:
				noOfPredictions=noOfPredictions+1
				W=1
			else:
				W=0
			if Team1=='LAC' or Team2=='LAC':
				print(Team1,row1[3],Team2,noOfPredictions,match)
				print("random")
			duplicate=playerRating
			playerRating=elo(playerRating,minutesPlayed,Team1,Team2,int(row1[4]),plusminus)
			m1=0
			m2=0
			for players in playerRating[Team1]:
				m1+=playerRating[Team1][players]*minutesPlayed[Team1][players]
			for players in playerRating[Team2]:
				m2+=playerRating[Team2][players]*minutesPlayed[Team2][players]
			TeamRating[Team1]=m1
			TeamRating[Team2]=m2
			match=match+1
			if Team1=='LAC' or Team2=='LAC':
				print("%%%%%%%%%%%% after update%%%%%%%%%%%%%%%")
				print("Updated rating for {}".format(Team1),round(m1))
				print("updated rating for {}".format(Team2),round(m2))
				print("Match number",match)
			sumTeam=0
			for Teeam in TeamRating:
				sumTeam=sumTeam+TeamRating[Teeam]
			print("Sum of team rating",sumTeam)
			if match==1230:
				print(TeamRating)
			#time.sleep(4)
		else:
			#print("Trying to repeat")
			#time.sleep(10)
			checklist.remove(c)
		
	#print("NEXT ROUND")
	i=i+1
csv_file1.close()
csv_file2.close()
	
