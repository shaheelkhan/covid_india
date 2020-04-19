# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 20:12:44 2020

@author: Shaheel
"""


#Libraries
import os
import glob
import urllib
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from datetime import datetime

###########################
#####  Web Scrapping  #####
###########################

def souper(base_url):
        url_page = urllib.request.urlopen(base_url)
        bsoup = BeautifulSoup(url_page,'html.parser')
        return bsoup

soup = souper("https://www.mohfw.gov.in/")

data=[]
for tr in soup.findAll('tr'):
        td = tr.findAll('td')
        row = [tr.text for tr in td]
        data.append(row)

#Create a Datafrae from the scrapped data
statedata=pd.DataFrame(data,columns=["Sl.No","State/UT","Confirmed","Recovered","Death"])

###########################
#####  Data Cleaning  #####
###########################

#Remove unwanted columns and rows
statedata.drop("Sl.No",axis=1,inplace=True)
statedata = statedata[:-3][1:]

statedata['State/UT'] = statedata['State/UT'].replace("Nagaland#","Nagaland")

#Function to return a csv file for daily updated data
def new_data(data):
        
        #Add a new date column that return today's date
        data['Date'] = pd.to_datetime('today')
        
        cols = ['Confirmed','Recovered','Death']
       
        #Change the datatype of numerical columns
        for col in cols:
                data[col] = data[col].astype(int)
        
        #Export today's data as a csv file
        today = pd.to_datetime('today').date()

        filename = today.strftime("%m-%d-%Y")+'.csv'
        filelocation = "C:\\Users\\Shaheel\\Desktop\\Covid19_India_Data\\covid_india\\"
        
        os.chdir("C:\\Users\\Shaheel\\Desktop\\Covid19_India_Data\\covid_india\\")
        
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
        
combined_data("C:\\Users\\Shaheel\\Desktop\\Covid19_India_Data\\covid_india\\")  
