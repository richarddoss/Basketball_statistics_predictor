from collections import defaultdict
import collections
import time
import re
import csv
def elo(fixedPlayer,playerRating,minutesPlayed,Team,OppTeam,TotTime,PTS):
	m1=0
	m2=0
	for players in playerRating[Team]:
		m1+=playerRating[Team][players]*minutesPlayed[Team][players]
	for players in playerRating[OppTeam]:
		m2+=playerRating[OppTeam][players]*minutesPlayed[OppTeam][players]
	m1without=m1-playerRating[Team][fixedPlayer]*minutesPlayed[Team][fixedPlayer]
	print("effective strength for {} player's team".format(fixedPlayer),m1without,"Effective strength for opp team",m2)
	minWithoutPlayer=minutesPlayed[Team][fixedPlayer]*int(TotTime)
	minWithPlayer=int(TotTime)-minWithoutPlayer
	PtTeam=minWithoutPlayer*m1without+minWithPlayer*m1
	PtOppTeam=int(TotTime)*m2
	print("PointProduction by {}".format(Team),PtTeam)
	print("PointProduction by {}".format(OppTeam),PtOppTeam)
	expectedValue=PtTeam-PtOppTeam
	print("update Value",PTS-expectedValue)
	time.sleep(10)
csv_file1 = open('TeamMatchups.csv', 'r')
reader1 = csv.reader(csv_file1)
i=0
j=0
minutesPlayed=defaultdict(dict)
playerRating=defaultdict(dict)
checklist=[]
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
							playerRating[Team1][row2[0]]=200
						else:
							minutesPlayed[Team2][row2[0]]=int(row2[5])/(int(row1[4]))
							playerRating[Team2][row2[0]]=200
				j=j+1
			j=0
			csv_file2.close()
			checklist.append(c)
			for fixedPlayer in playerRating[Team1]:
				elo(fixedPlayer,playerRating,minutesPlayed,Team1,Team2,row1[4],int(row1[6]))
			print("opp team update")
			for fixedPlayer in playerRating[Team2]:
				elo(fixedPlayer,playerRating,minutesPlayed,Team2,Team1,row1[4],-1*int(row1[6]))
		else:
			print("Trying to repeat")
			checklist.remove(c)
		
	print("NEXT ROUND")
	i=i+1
csv_file1.close()
csv_file2.close()
	
