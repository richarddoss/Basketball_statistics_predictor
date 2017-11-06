from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import collections
import time
import csv
Teams=['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEL','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','SAC','SAS','TOR','UTA','WAS']
driver= webdriver.Firefox()
driver.get('http://stats.nba.com/search/team-game/#?CF=PTS*gt*20&sort=GAME_DATE&dir=-1&Season=2016-17&SeasonType=Regular%20Season,Pre%20Season')
#runBtn=driver.find_element_by_xpath('/html/body/div[3]/div[2]/section/div/div[2]/div/div[2]/stats-run-it/button')
#runBtn.click()
time.sleep(30)
matches=2664
count=50
while count<=matches:
    LoadMoreBtn=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[2]/div/a')
    LoadMoreBtn.click()
    count=count+50
    time.sleep(10)
p=0
NoOfColumn=25
csv_file = open('RegularSeasonteamstats.csv', 'w')
writer = csv.writer(csv_file)
ColumnTitle=['TEAM', 'DATE', 'MATCHUP', 'W/L', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', '+/-']
writer.writerow(['TEAM', 'DATE', 'MATCHUP', 'W/L', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', '+/-'])
for i in range(1,2829):
    teams_dict = collections.OrderedDict()
    for j in range(1,NoOfColumn):
        data=driver.find_element_by_xpath('/html/body/div[3]/div/div/div[4]/nba-stat-table/div[1]/div[1]/table/tbody/tr['+str(i)+']/td['+str(j)+']')
        #print(data.text)
        teams_dict[ColumnTitle[j-1]] = data.text
    writer.writerow(teams_dict.values())
    print(i)
csv_file.close()
driver.close()