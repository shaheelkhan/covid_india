# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 20:12:44 2020

@author: Shaheel
"""


#Libraries

import os
import glob
import pandas as pd
import datetime




#Create a Dataframe
statedata=pd.read_json('https://www.mohfw.gov.in/data/datanew.json')

#Data Cleaning

key = lambda x: x != 'state_name'
statedata = statedata[sorted(statedata, key = key)]

#Rename some columns
statedata = statedata.rename(columns= {'positive':'confirmed','cured':'recovered'})

#Remove last two columns
statedata = statedata.drop(['sno','state_code'],axis=1)

#Remove last row
statedata = statedata[0:36]



#Check for missing data
statedata.isnull().sum()


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


