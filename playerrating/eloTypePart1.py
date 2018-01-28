from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import collections
import time
import re
import csv
csv_file1 = open('TeamMatchups.csv', 'r')
reader1 = csv.reader(csv_file1)
i=0
j=0
for row1 in reader1:
	if i>0:
		s=re.split('\W+',row1[2])
		#print(s)
		if len(s)==2:
			Team1=s[0]
			Team2=s[1]
		else:
			Team1=s[0]
			Team2=s[2]
		#print(row1[1],Team1,Team2,i)
		csv_file2 = open('PlayerDetails.csv', 'r')
		reader2 = csv.reader(csv_file2)
		for row2 in reader2:
			if j>0:
				if (Team1==row2[1] or Team2==row2[1]) and row1[1]==row2[2]:
					print(row2[0],"playername",row2[1],"team",row2[2],"date")
					time.sleep(10)
			j=j+1
		csv_file2.close()
			
	i=i+1
csv_file1.close()
csv_file2.close()
	
