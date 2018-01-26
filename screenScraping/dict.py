from collections import defaultdict
import csv
import pandas as pd
import re
import numpy as np
import time
dataFile=open('tests.csv','r')
reader=csv.reader(dataFile)
player_rating= defaultdict(dict)
LenTeams=defaultdict(dict)
i=0
Teams=['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','SAC','SAS','TOR','UTA','WAS']
for row in reader:
	#print(row[24])
	player_rating[row[1]][row[0]]=200
dataFile.close()
dataFile=open('tests.csv','r')
reader=csv.reader(dataFile)
for i in range(0,30):
	LenTeams[Teams[i]]=len(player_rating[Teams[i]])
for i in range(0,30):
	for team in player_rating[Teams[i]]:
		player_rating[Teams[i]][team]=(1000/(LenTeams[Teams[i]]))
		print(team,player_rating[Teams[i]][team])
		
# Intializiation of rating is done
j=0
K=0.05
time.sleep(10)
for row in reader:
	if j!=0:
		#print("hi")
		actualScore=player_rating[row[1]][row[0]]
		s=re.split('\W+',row[3])
		#print("hello")
		#print(s)
		if len(s)==2:
			if row[1]==s[0]:
				oppTeam=s[1]
			else:
				oppTeam=s[0]
		else:
			if row[1]==s[0]:
				oppTeam=s[2]
			else:
				oppTeam=s[0]
		#finding the team rating
		TeamRating=0
		for player in player_rating[row[1]]:
			TeamRating+=player_rating[row[1]][player]
		#print(TeamRating,row[1])
		OppTeamRating=0
		for team in player_rating[oppTeam]:
			OppTeamRating+=player_rating[oppTeam][team]
		expectedScore=OppTeamRating-((LenTeams[oppTeam]-1)/LenTeams[oppTeam])*TeamRating
		X=actualScore-expectedScore
		print(OppTeamRating,"OppTeamRating",oppTeam)
		print(TeamRating,"TeamRating",row[1])
		if TeamRating>OppTeamRating:
			print("Expected win",row[1])
		else:
			print("expected win",oppTeam)
		if row[4]=="W":
			print("actual win",row[1])
		else:
			print("actual win",oppTeam)
		#print(row[4])
		print("player name",row[0])
		print(actualScore,"actual")
		print(expectedScore,"expected")
		player_rating[row[1]][row[0]]=player_rating[row[1]][row[0]]+K*int(row[24])*abs(X)
		#print(row[1],player,player_rating[row[1]][player])
		time.sleep(10)
	else:
		j=1
#rating update
#print(player_rating[Teams[i]])
'''for row in reader:
	ActualScore=int(player_rating[row[1]][row[0]])
	for team in player_rating[row[1]]
		print(team)'''

'''
new_dic['BOS']['Richard']=234
new_dic['BOS']['Einstein']=200
new_dic['ATL']['David']=100
for dic in new_dic['BOS']:
    print(dic,new_dic['BOS'][dic])'''

