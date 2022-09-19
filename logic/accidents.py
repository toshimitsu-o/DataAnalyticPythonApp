#python file for class Accident and related functions

#import pandas, datetime and numpy modules
import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3
from database import queries


#creating a dataframe
con = sqlite3.connect("database/accidentDatabase.sqlite")
df = pd.read_sql_query("SELECT *", con)


def get_hour(string):
#Gets hour from datestring
    hr = datetime.fromisoformat(string).hour
    return hr

    
#Calculates the average number of accidents in each hour of the day.
def hourly_average(df): #df is the accident data (list of tuple)

    time = []
    time = df.sort_values(by=['ACCIDENT_TIME'])
    for i in time:
        time.append
    return time 

#test
#df = hourly_average(df)
#print(df)
#NOT WORKING


#Calculate the number of accidents in each accident type.
def accident_type(df): 
    type = df['ACCIDENT_TYPE'].value_counts(ascending=True)
    return type

#test 
#df = accident_type(df)
#print(df)
#WORKING

#Calculates the number of accidents in each month.
def calculate_by_month(df):
    df['ACCIDENT_DATE']= pd.to_datetime(df['ACCIDENT_DATE'])
    result = df.groupby([df['ACCIDENT_DATE'].dt.year, df['ACCIDENT_DATE'].dt.month]).agg({'ABS_CODE':sum})
    return result

#test
#df = calculate_by_month(df)
#print(df)
#PARTIALLY WORKING


#Calculates the number of accidents in each day.
def calculate_by_day(df): 
    day = df['DAY_OF_WEEK'].value_counts(ascending=True)
    return day

#test 
#df = calculate_by_day(df)
#print(df)
#WORKING

#Calculates the number of accidents in each LGA.
def calculateLGA(df):
    LGA = df['LGA_NAME'].value_counts(ascending=True)
    return LGA
    
#test 
#df = calculateLGA(df)
#print(df)
#WORKING

#Calculates the number of accidents in each region.
def calculate_region(df):
    region = df['REGION_NAME'].value_counts(ascending=True)
    return region
        
#test
#df = calculate_region(df)
#print(df)
#WORKING
    

