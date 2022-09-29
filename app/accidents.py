#python file for class Accident and related functions

#import pandas, datetime and numpy modules
import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3


#creating a dataframe
# con = sqlite3.connect("database/accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
# cur = con.cursor()
# cur.execute("SELECT * FROM Accidents")
# rows = cur.fetchall()
#print(rows[1:3])

# def connection():
#     """creates sqlite connection to accidentDatabase
#     """
#     con = sqlite3.connect("database/accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
#     cur = con.cursor()

##Calculates the average number of accidents in each hour of the day.
def hourly_average():
    connection = sqlite3.connect("app/accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    time = pd.read_sql("SELECT accidentTime from Accident", connection)
    
    # for i in date:
    #     for j in time:
    #         fullDate.append(date[i]+ " " + time[j])
    #         print(type(fullDate))
    #         print(fullDate)
            
    return time
    # hourly_average = pd.read_sql("SELECT CAST(FLOOR(CAST(accidentDate AS float)) AS datetime) AS Day, DATEPART(hh, accidentTime) AS hour, AVG(COUNT(AccidentNo)) AS average FROM Accident GROUP BY CAST(FLOOR(CAST(accidentDate AS float)) AS datetime), DATEPART(hh, accidentDate);", connection)
    # return hourly_average
    #NOT WORKING 

#test
# test = hourly_average()
# print(test)
#NOT WORKING


#Calculate the number of accidents in each accident type.
def accident_type():
    connection = sqlite3.connect("app/accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    accidents = pd.read_sql("SELECT accidentType, COUNT(*) FROM Accident GROUP BY accidentType ORDER BY COUNT(*) DESC ;", connection)
    return accidents

#OLD VERSION WITH PANDAS 
#Calculate the number of accidents in each accident type.
#def accident_type(rows): 
    #type = rows['ACCIDENT_TYPE'].value_counts(ascending=True)
    #return type

#test 
#test = accident_type()
#print(test)
#WORKING

#Calculates the number of accidents in each month.
def calculate_by_month():
    connection = sqlite3.connect("app/accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    accidents_each_month = pd.read_sql("SELECT EXTRACT(YEAR FROM accidentDate) AS Year, EXTRACT(MONTH FROM accidentDate) AS Month FROM Accident;", connection)
    return accidents_each_month
    # Logically this should work.


#OLD VERSION WITH PANDAS
#Calculates the number of accidents in each month.
#def calculate_by_month(df):
    #df['ACCIDENT_DATE']= pd.to_datetime(df['ACCIDENT_DATE'])
    #result = df.groupby([df['ACCIDENT_DATE'].dt.year, df['ACCIDENT_DATE'].dt.month]).agg({'ABS_CODE':sum})
    #return result

#test
#test = calculate_by_month()
#print(test)
#PARTIALLY WORKING

#Calculates the number of accidents in each day.
def calculate_by_day():
    connection = sqlite3.connect("app/accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    by_day = pd.read_sql("SELECT dayOfWeek, COUNT(*) FROM Accident GROUP BY dayOfWeek ORDER BY COUNT(*) DESC ;", connection)
    return by_day


#OLD VERSION WITH PANDAS 
#Calculates the number of accidents in each day.
#def calculate_by_day(df): 
    #day = df['DAY_OF_WEEK'].value_counts(ascending=True)
    #return day

#test 
#test = calculate_by_day()
#print(test)
#WORKING

#Calculates the number of accidents in each LGA.
def calculateLGA():
    connection = sqlite3.connect("app/accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    LGA = pd.read_sql("SELECT lgaName, COUNT(*) FROM Accident GROUP BY lgaName ORDER BY COUNT(*) DESC ;", connection)
    return LGA

#OLD VERSION WITH PANDAS
#Calculates the number of accidents in each LGA.
#def calculateLGA(df):
    #LGA = df['LGA_NAME'].value_counts(ascending=True)
    #return LGA
    
#test 
#test = calculateLGA()
#print(test)
#WORKING

#Calculates the number of accidents in each region.
def calculate_region():
    connection = sqlite3.connect("app/accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    region = pd.read_sql("SELECT regionName, COUNT(*) FROM Accident GROUP BY regionName ORDER BY COUNT(*) DESC ;", connection)
    return region

#OLD VERSION WITH PANDAS
#Calculates the number of accidents in each region.
#def calculate_region(df):
    #region = df['REGION_NAME'].value_counts(ascending=True)
    #return region
        
#test
#test = calculate_region()
#print(test)
#WORKING


    

