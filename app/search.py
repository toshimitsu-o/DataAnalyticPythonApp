"""Class defines a search"""

import sqlite3
from sqlite3 import Error
from typing_extensions import Self
import pandas as pd

from accidents import hourly_average

def connection():
    """creates sqlite connection to accidentDatabase
    """
    con = sqlite3.connect("accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    return con

class Search: 
    def __init__(self, To_Date = None, From_Date = None, Accident_Type_Keyword = None, Accident_Type_List = None, Output_Type = None, Lga = None, Region = None):
        self.To_Date = To_Date
        self.From_Date = From_Date
        self.Accident_Type_Keyword = Accident_Type_Keyword
        self.Accident_Type_List = Accident_Type_List
        self.Output_Type = Output_Type
        self.Lga = Lga
        self.Region = Region
    
    def getResult(self):
        """
        Get database records with the search criteria
        """
        # Set all search criteria to prepare sql query
        if self.From_Date:
            date1 = str(self.From_Date)
        else:
            date1 = "2013-07-01"
        if self.To_Date:
            date2 = str(self.To_Date)
        else:
            date2 = "2019-02-01"

        try:
            con = connection()
            cur = con.cursor()
            sql = """SELECT * FROM Accident WHERE accidentDate BETWEEN ? AND ?"""
            data = (date1, date2)
            cur.execute(sql, data)  
            result = cur.fetchall()
            return result
        except Error as e:
            print(e)

    def dataRowsCount(self):
        """
        To count the rows in the database.
        """
        rows = self.getResult()
        i = 0
        for r in rows:
            i+=1
        return i

    def listAccidentType(self):
        """Generate and return a list of accident types in the database"""
        # find distinct accident type values in the database
        # return list
        pass

    def matchAccidentType(self):
        """Find a match with keyword and return the matched Accident type as string"""
        word = self.Accident_Type_Keyword
        # types = self.listAccidentType()
        # find a match (maybe use re module for regular expression)
        pass

    
    def hourly_average(self):
        """Calculates the average number of accidents in each hour from the search result and return data for generating a plot"""
        result = self.getResult(self)
        hourlyAccidentDict = dict()
        for hour in result["accidentTime"]:
             hourlyAccidentDict[hour[0:1]] += 1
        hourlyAvg = []
        for hour in hourlyAccidentDict:
            hourlyAvg.append((hourlyAccidentDict.get(hour), hourlyAccidentDict.get(hour)/len(result)))
        return hourlyAvg
        
        # Extract ACCIDENT_TIME into (maybe) list

        #  Create dic and go through the list
        # extract only hour (first two number) and add to the dict using hour as key and value += 1

        # (maybe) convert the dict to tuple for plot module
        # return the data
    
    def accident_type():
        """Calculate the number of accidents in each accident type."""
        connection = sqlite3.connect("app/accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        accidents = pd.read_sql("SELECT accidentType, COUNT(*) FROM Accident GROUP BY accidentType ORDER BY COUNT(*) DESC ;", connection)
        # Needs to query with criteria in search object: self
        # Use dummy search object within the function and test by print
        return accidents
    
    def calculate_by_month():
        """Calculates the number of accidents in each month."""
        
        connection = sqlite3.connect("app/accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        accidents_each_month = pd.read_sql("SELECT EXTRACT(YEAR FROM accidentDate) AS Year, EXTRACT(MONTH FROM accidentDate) AS Month FROM Accident;", connection)
        return accidents_each_month
        # Needs to use criteria in search object: self
    
    def calculate_by_day():
        """Calculates the number of accidents in each day."""
        connection = sqlite3.connect("app/accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        by_day = pd.read_sql("SELECT dayOfWeek, COUNT(*) FROM Accident GROUP BY dayOfWeek ORDER BY COUNT(*) DESC ;", connection)
        return by_day
        # Needs to use criteria in search object: self

    def calculateLGA():
        """alculates the number of accidents in each LGA"""
        connection = sqlite3.connect("app/accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        LGA = pd.read_sql("SELECT lgaName, COUNT(*) FROM Accident GROUP BY lgaName ORDER BY COUNT(*) DESC ;", connection)
        return LGA
        # Needs to use criteria in search object: self
    
    def calculate_region():
        """Calculates the number of accidents in each region."""
        connection = sqlite3.connect("app/accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        region = pd.read_sql("SELECT regionName, COUNT(*) FROM Accident GROUP BY regionName ORDER BY COUNT(*) DESC ;", connection)
        return region
        # Needs to use criteria in search object: self
        
        
        
x = Search.hourly_average()

print(x)