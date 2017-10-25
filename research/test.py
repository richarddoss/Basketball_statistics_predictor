from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import collections
import time
import csv
Teams=['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEL','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','SAC','SAS','TOR','UTA','WAS']
driver= webdriver.Firefox()
driver.get('http://stats.nba.com/search/team-game/#?CF=PTS*gt*20&sort=GAME_DATE&dir=1&Season=2016-17&GB=Y')
time.sleep(30)
filtersTab=driver.find_element_by_xpath('/html/body/div[3]/div[2]/section/div/div[2]/div/div[2]/button')
filtersTab.click()
teamTab=driver.find_element_by_xpath('/html/body/div[3]/div[2]/section/div/div[3]/div/div/form/div/section[2]/div/div[3]/div/div[4]')
teamTab.click()
selectTeam=driver.find_element_by_xpath('/html/body/div[3]/div[2]/section/div/div[3]/div/div/form/div/section[2]/div/div[2]/ul/li['+str(5)+']')
selectTeam.click()
runBtn=driver.find_element_by_xpath('/html/body/div[3]/div[2]/section/div/div[2]/div/div[2]/stats-run-it/button')
runBtn.click()
time.sleep(20)
for i in range(1,4):
    LoadMoreBtn = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[4]/nba-stat-table/div[2]/div/a')
    print(LoadMoreBtn)
    LoadMoreBtn.click()
