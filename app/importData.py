from time import strptime
from wsgiref.validate import validator
import pandas as pd
#import csv
from pycsvschema.checker import Validator
#import sys
import datetime
from distutils.util import strtobool
import sqlite3
from sqlite3 import Error
import shutil

def performImport(fileName):
    """Copy file (parameter) to the local directory and insert the data into database"""
    src = fileName
    dst = "imported.csv"
    shutil.copy(src, dst)
    createDatabase()
    insertData(dst)

def validateFile(fileName):
    
    """function accepts csv file, performs schema valiation and determines if data is valid for processing 
    """
    # attempts to validate csv file
    try:
        # list of required fields
        schema = {
            "fields": [
                {
                    "name": "ACCIDENT_NO",
                    "required": True
                },
                {
                    "name": "ACCIDENT_DATE",
                    "required": True
                },
                {
                    "name": "ACCIDENT_TIME",
                    "required": True
                },
                {
                    "name": "ACCIDENT_TYPE",
                    "required": True
                },
                {
                    "name": "DAY_OF_WEEK",
                    "required": True
                },
                {
                    "name": "SEVERITY",
                    "required": True
                },
                {
                    "name": "LONGITUDE",
                    "required": True
                },
                {
                    "name": "LATITUDE",
                    "required": True
                },
                {
                    "name": "LGA_NAME",
                    "required": True
                },
                {
                    "name": "REGION_NAME",
                    "required": True
                },
                {
                    "name": "FATALITY",
                    "required": True
                },
                {
                    "name": "SERIOUSINJURY",
                    "required": True
                },
                {
                    "name": "ALCOHOL_RELATED",
                    "required": True
                },
            ]
        }
        # validates csv file against listed schema
        v = Validator(fileName, schema=schema)
        v.validate()
        
    # if validation fails returns this error
    except:
        return "validation error"
            
    # if validation is successful this code will execute
def importData(fileName):
    
    try:
        validateFile(fileName)
    except:
        return "CSV file not valid"
    else:
        wb = pd.read_csv(fileName)
        accidentData = []

        # iterates through each row and appends required field information as a tuple to the list accidentData
        for index, row in wb.iterrows():
            aNo = row[1]
            # converts dates from dd/mm/yyyy to yyyy-mm-dd format output is a string
            aDate = datetime.datetime.strptime(row[4], "%d/%m/%Y").strftime("%Y-%m-%d")
            # aFDate = datetime.datetime.strptime(aDate, "%Y-%m-%d").date()
            # # print(aFDate)
            # # print(type(aFDate))
            # converts time from hh.mm.ss to hh:mm:ss format
            aTime = row[5]
            aFTime = ""
            for i in aTime:
                if i ==".":
                    aFTime += ":"
                else:
                    aFTime += i
            # aPTime = datetime.datetime.strptime(aFTime, "%H:%M:%S").time()
            aType = row[7]
            dayOfWeek = row[8]
            severity = row[14]
            longitude = row[18]
            latitude = row[19]
            lgaName = row[21]
            regionName = row[22]
            fatality = row[27]
            seriousInjury = row[28]
            # converts results to boolean 0,1
            alcoholRelated = strtobool(row[45])
            accidentData.append((aNo, aDate, aFTime, aType, dayOfWeek, severity, longitude, latitude, lgaName, regionName, fatality, seriousInjury, alcoholRelated))

        return accidentData
    
    
def createDatabase():
    """ create a database connection to a SQLite database """
    connection = None
    try:
        connection = sqlite3.connect("accidentDatabase.db")
        c = connection.cursor()
        c.execute(
            "DROP TABLE IF EXISTS Accident;")
        c.execute("""CREATE TABLE IF NOT EXISTS Accident
            (accidentNo VARCHAR PRIMARY KEY,
            accidentDate TEXT,
            accidentTime TEXT,
            accidentType VARCHAR,
            dayOfWeek TEXT,
            severity VARCHAR,
            longitude REAL,
            latitude REAL,
            lgaName VARCHAR,
            regionName VARCHAR,
            fatalites INT,
            seriousInjuries INT,
            alcoholRelated INT);"""
        )
    except Error as e:
        return e
        
   
def insertData(dataFileName):
    """attempts to insert data into a database 

    Args:
        dataFileName (str): filepath of csv for import
    """
    connection = None
    try:
        connection = sqlite3.connect("accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        c = connection.cursor()
        data = importData(dataFileName)
        c.executemany("INSERT INTO Accident VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", data)
        connection.commit()
        
    except Error as e:
        print(e)
        
# def getDateRange():
#     """queries accident database and returns tuple of (minDate, maxDate)
#     """
    
#     connection = sqlite3.connect("accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
#     c = connection.cursor()
#     sqlmin = "SELECT MIN(accidentDate) FROM Accident;"
#     sqlmax = "SELECT MAX(accidentDate) FROM Accident;"
#     c.execute(sqlmin)
#     minDate = c.fetchall()
#     c.execute(sqlmax)
#     maxDate = c.fetchall()
#     return (minDate, maxDate)

# def getAccidentTypes():
#     """queries accident database and returns a list of all unique accident types
#     """
#     connection = sqlite3.connect("accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
#     accidents = pd.read_sql("SELECT accidentType FROM Accident;", connection)
#     accidentTypes = accidents["accidentType"].unique()
#     # converts from numpy.ndarray to list type
#     accidentList = []
#     for i in accidentTypes:
#         accidentList.append(i)
#     return accidentList

# x = getAccidentTypes()
# print(x)
# print(type(x))

# createDatabase()
# insertData("C:/Users/zeefe/OneDrive/Documents/Uni/Year 2/Trimester 2/Software Technologies/Git Repositories/2810ICT-2022-Assignment/2810ICT-2022-Assignment/dataset/Crash Statistics Victoria.csv")