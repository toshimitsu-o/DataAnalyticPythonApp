import sqlite3
from sqlite3 import Error

def emptyTable():
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
    else:
        print("Table empty")

emptyTable()