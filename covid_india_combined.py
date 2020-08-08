# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 20:12:44 2020

@author: Shaheel
"""


#Libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import glob
import urllib
import pandas as pd
import datetime
from datetime import datetime

#Page to scrap
url = "https://www.mohfw.gov.in/"

#Create a new Chrome session
chromedriver = "C:\\webdrivers\\chromedriver.exe"
driver = webdriver.Chrome(chromedriver)
driver.implicitly_wait(30)
driver.get(url)

python_button = driver.find_element_by_id('state-data')
python_button.click()


###########################

#####  Web Scrapping  #####

###########################

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

data=[]
for tr in soup.findAll('tr'):
        td = tr.findAll('td')
        row = [tr.text for tr in td]
        data.append(row)
        

#Create a Datafrae from the scrapped data
statedata=pd.DataFrame(data,columns=["Sl.No","State/UT","Active","Active_Change","Recovered","Recovered_Change","Death","Death_Change"])


#Data Cleaning

statedata.drop("Sl.No",axis=1,inplace=True)
statedata = statedata[3:38]

for col in statedata.columns:
        statedata[col] = statedata[col].replace("\xa0 ",0)
        
for col in statedata.columns:
        statedata[col] = statedata[col].str.replace("#","")

#Check for missing data
statedata.isnull().sum()

#Replace NaN with 0
statedata = statedata.fillna(0)

for col in statedata.columns:
        if col != 'State/UT':
                statedata[col] =  statedata[col].astype(int)


#Add a new column for Total confirmed cases
statedata['Confirmed'] = statedata['Active'] + statedata['Recovered'] + statedata['Death']


#Function to return a csv file for daily updated data
def new_data(data):
        
        #Add a new date column that return today's date
        data['Date'] = pd.to_datetime('today')
        
        #Export today's data as a csv file
        today = pd.to_datetime('today').date()

        filename = today.strftime("%m-%d-%Y")+'.csv'
        filelocation = os.getcwd()
        filelocation = filelocation + '\\'
        
        os.chdir(filelocation)
        
        extension = 'csv'
        all_filenames = [file for file in glob.glob('*.{}'.format(extension))]
        
        if filename in all_filenames:
                os.remove(filelocation+filename)
               
        return data.to_csv(filelocation + filename,index=False)

new_data(statedata)

#Function to combine each days data into a single csv file
def combined_data(path):
        
        os.chdir(path)
        
        extension = 'csv'
        
        all_filenames = [file for file in glob.glob('*.{}'.format(extension))]
        
        if 'combined.csv' in all_filenames:
                os.remove(path+'combined.csv')
        
        all_filenames = [file for file in glob.glob('*.{}'.format(extension))]
        
        combined = pd.concat([pd.read_csv(f) for f in all_filenames],sort=False)
        
        return combined.to_csv('combined.csv',index=False,encoding='utf-8-sig')        
        
location = os.getcwd()
location = location + '\\'        

combined_data(location)   