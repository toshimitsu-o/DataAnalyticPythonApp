
import sqlite3
from sqlite3 import Error
from importData import *

def createDatabase(dbFile):
    """ create a database connection to a SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(dbFile)
        c = connection.cursor()
        c.execute(
            """DROP TABLE IF EXISTS Accident;
            CREATE TABLE IF NOT EXISTS Accident
            (ACCIDENT_NO VARCHAR(20) PRIMARY KEY,
            ACCIDENT_DATE TEXT,
            ACCIDENT_TIME TEXT,
            ACCIDENT_TYPE VARCHAR(30),
            DAY_OF_WEEK TEXT,
            SEVERITY VARCHAR(30),
            LONGITUDE REAL,
            LATITUDE REAL,
            LGA_NAME VARCHAR(30),
            REGION_NAME VARCHAR(30),
            FATALITY BOOLEAN,
            SERIOUSINJURY BOOLEAN,
            ALCOHOL_RELATED BOOLEAN);"""
        )
    except Error as e:
        print(e)
        
def insertData(dbFile, values):
    """attempts to insert data into a database 

    Args:
        dbFile (_type_): _description_
    """
    connection = None
    try:
        connection = sqlite3.connect(dbFile)
        c = connection.cursor()
        c.execute(
            """"""
        )
    except Error as e:
        print(e)
        
        
        
createDatabase('testDatabase.db')

