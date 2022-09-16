
import sqlite3
from sqlite3 import Error
from importData import importFile

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
        print(e)
        
   
def insertData(dataFileName):
    """attempts to insert data into a database 

    Args:
        dataFileName (str): filepath of csv for import
    """
    connection = None
    try:
        connection = sqlite3.connect("accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        c = connection.cursor()
        data = importFile(dataFileName)
        c.executemany("INSERT INTO Accident VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", data)
        connection.commit()
        
    except Error as e:
        print(e)
        
        
        
createDatabase()
insertData("C:/Users/zeefe/OneDrive/Documents/Uni/Year 2/Trimester 2/Software Technologies/Git Repositories/2810ICT-2022-Assignment/2810ICT-2022-Assignment/dataset/Crash Statistics Victoria.csv")

