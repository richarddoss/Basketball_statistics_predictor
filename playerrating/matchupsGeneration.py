from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import collections
import time
import csv
driver= webdriver.Firefox()
driver.get('http://stats.nba.com/search/team-game/#?Season=2017-18&SeasonType=Regular%20Season&sort=GAME_DATE&dir=-1')
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
csv_file = open('TeamMatchups2017-18.csv', 'w')
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

