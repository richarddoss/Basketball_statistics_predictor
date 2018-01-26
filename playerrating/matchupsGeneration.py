from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import collections
import time
import csv
driver= webdriver.Firefox()
driver.get('http://stats.nba.com/search/team-game/#?sort=GAME_DATE&dir=-1&Season=2016-17&SeasonType=Regular%20Season&DateFrom=10%2F25%2F2016&DateTo=04%2F12%2F2017')
time.sleep(10)
crossBtn=driver.find_element_by_xpath('/html/body/div[3]/div[2]/section/div/div[2]/div/div[1]/div/div/table/tbody/tr/td[4]/button')
crossBtn.click()
runBtn=driver.find_element_by_xpath('/html/body/div[3]/div[2]/section/div/div[2]/div/div[2]/stats-run-it/button')
runBtn.click()
time.sleep(30)
totalGames = "2460"
print(totalGames)
numberClicks=int(int(totalGames)/50)
if int(totalGames)%50==0:
	numberClicks=numberClicks-1
for i in range(0,numberClicks):
        LoadMoreBtn = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[2]/div/a')
        LoadMoreBtn.click()
csv_file = open('TeamMatchups.csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(['TEAM', 'DATE', 'MATCHUP', 'W/L', 'MIN', 'PTS', '+/-'])
for row in range(1,2461):
	teams_dict = collections.OrderedDict()
	teams_dict['TEAM']=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr['+str(row)+']/td[1]/a').text
	teams_dict['DATE']=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr['+str(row)+']/td[2]').text
	teams_dict['MATCHUP']=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr['+str(row)+']/td[3]/a').text
	teams_dict['W/L']=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr['+str(row)+']/td[4]').text
	teams_dict['MIN']=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr['+str(row)+']/td[5]').text
	teams_dict['PTS']=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr['+str(row)+']/td[6]').text
	teams_dict['+/-']=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr['+str(row)+']/td[24]').text
	writer.writerow(teams_dict.values())
	print('row number',row)
csv_file.close()
driver.close()
'''
/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr[1]/td[24]

/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr[1]/td[2]
/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr[1]/td[4]
/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr[1]/td[1]/a
/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr[2]/td[1]/a
/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr[1]/td[24]
/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr[2460]/td[1]/a
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
    runBtn=driver.find_element_by_xpath('/html/body/div[3]/div[2]/section/div/div[2]/div/div[2]/stats-run-it/button')
    runBtn.click()
    time.sleep(20)
    totalGames = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[4]/nba-stat-table[1]/div[1]/div[1]/table/tbody/tr/td[2]')

    print(totalGames.text)
    numberClicks=int(int(totalGames.text)/50)
    if int(totalGames.text)%50==0:
        numberClicks=numberClicks-1
    for i in range(0,numberClicks):
        LoadMoreBtn = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[2]/div/a')
        LoadMoreBtn.click()
    #/html/body/div[3]/div[2]/section/div/div[3]/div/div/form/div/section[2]/div/div[2]/ul/li[3]
    #/html/body/div[3]/div[2]/section/div/div[3]/div/div/form/div/section[2]/div/div[2]/ul/li[4]
    time.sleep(10)
    p=0
    NoOfColumn=24
    csv_file = open(Teams[teamIndex-3]+'teamstats.csv', 'w')
    writer = csv.writer(csv_file)
    ColumnTitle=['TEAM', 'DATE', 'MATCHUP', 'W/L', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', '+/-']
    writer.writerow(['TEAM', 'DATE', 'MATCHUP', 'W/L', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', '+/-'])

    for i in range(1,int(totalGames.text)):
        teams_dict = collections.OrderedDict()
        for j in range(1,NoOfColumn):
            data=driver.find_element_by_xpath('/html/body/div[3]/div/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr['+str(i)+']/td['+str(j)+']')
            #print(data.text)
            teams_dict[ColumnTitle[j]] = data.text
        writer.writerow(teams_dict.values())
    csv_file.close()
driver.close()
'''
