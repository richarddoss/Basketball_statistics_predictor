from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import collections
import time
import csv
Teams=['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEL','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','SAC','SAS','TOR','UTA','WAS']
driver= webdriver.Firefox()
driver.get('http://stats.nba.com/search/player-game/#?sort=GAME_DATE&dir=-1&SeasonType=Regular%20Season&DateFrom=04%2F01%2F2017&DateTo=04%2F12%2F2017')

time.sleep(30)
crossBtn=driver.find_element_by_xpath('/html/body/div[3]/div[2]/section/div/div[2]/div/div[1]/div/div/table/tbody/tr/td[4]/button')
crossBtn.click()
'''
for teamIndex in range(3,33):
    filtersTab=driver.find_element_by_xpath('/html/body/div[3]/div[2]/section/div/div[2]/div/div[2]/button')
    filtersTab.click()
    teamTab=driver.find_element_by_xpath('/html/body/div[3]/div[2]/section/div/div[3]/div/div/form/div/section[2]/div/div[3]/div/div[4]')
    teamTab.click()
    if teamIndex!=3:
        cancelTeam = driver.find_element_by_xpath('/html/body/div[3]/div[2]/section/div/div[3]/div/div/form/div/section[2]/div/div[2]/ul/li[' + str(teamIndex-1) + ']')
        cancelTeam.click()
    selectTeam=driver.find_element_by_xpath('/html/body/div[3]/div[2]/section/div/div[3]/div/div/form/div/section[2]/div/div[2]/ul/li['+str(teamIndex)+']')
    selectTeam.click()
'''
runBtn=driver.find_element_by_xpath('/html/body/div[3]/div[2]/section/div/div[2]/div/div[2]/stats-run-it/button')
runBtn.click()
time.sleep(20)
totalGames = 1993
print(totalGames)
numberClicks=int(int(totalGames)/50)
#numberClicks=numberClicks-1
#numberClicks=9
for i in range(0,numberClicks):
	LoadMoreBtn = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[2]/div/a')
	LoadMoreBtn.click()
	print("Number of clicks",i)
	time.sleep(10)
p=0
NoOfColumn=26
csv_file = open('tests.csv', 'a')
writer = csv.writer(csv_file)
ColumnTitle=['PLAYER','TEAM', 'DATE', 'MATCHUP', 'W/L', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', '+/-']
#writer.writerow(['PLAYER','TEAM', 'DATE', 'MATCHUP', 'W/L', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', '+/-'])
for i in range(1,int(totalGames)):
	print("tsabl",i)
	teams_dict = collections.OrderedDict()
	for j in range(1,NoOfColumn):
		data=driver.find_element_by_xpath('/html/body/div[3]/div/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr['+str(i)+']/td['+str(j)+']')
            #print(data.text)
#/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr[1]/td[25]
		teams_dict[ColumnTitle[j-1]] = data.text
	
	writer.writerow(teams_dict.values())
csv_file.close()
driver.close()
