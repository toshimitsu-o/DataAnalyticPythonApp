"""Class defines a search"""

import sqlite3
from sqlite3 import Error
import pandas as pd
import re as r

# from app.importData import getDateRange

# from accidents import hourly_average

def connection():
    """creates sqlite connection to accidentDatabase
    """
    con = sqlite3.connect("accidentDatabase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
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
    
    def getDateRange(self):
        """queries accident database and returns tuple of (minDate, maxDate)
        """
    
        connection = connection()
        c = connection.cursor()
        sqlmin = "SELECT MIN(accidentDate) FROM Accident;"
        sqlmax = "SELECT MAX(accidentDate) FROM Accident;"
        c.execute(sqlmin)
        minDate = c.fetchall()
        c.execute(sqlmax)
        maxDate = c.fetchall()
        return (minDate, maxDate)
    
    
    def getResult(self):
        """
        Get database records with the search criteria
        """
        # Set all search criteria to prepare sql query
        # connection = connection()
        # dateRange = self.getDateRange()
        # minDate = dateRange[0]
        # maxDate = dateRange[1]
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
            sql = """SELECT * FROM Accident WHERE accidentDate BETWEEN ? AND ?;"""
            data = (date1, date2)
            cur.execute(sql, data)  
            result = cur.fetchall()
            return result
            # print(type(result))
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
    
    def getTotalDays(self):
        """queries database and returns a list of the difference between To_date and For_Date

        Returns:
            list: list of one int
        """
        con = connection()
        cur = con.cursor()
        sql = "SELECT CAST((JULIANDAY(?) - JULIANDAY(?) + 1) AS Integer);"
        data = [self.To_Date, self.From_Date]
        cur.execute(sql, data)
        result = cur.fetchone()
        return result

    def listAccidentType(self):
        """queries accident database and returns a list of all unique accident types
        """
        try:
            con = connection()
            accidents = pd.read_sql("SELECT accidentType FROM Accident;", connection)
            accidentTypes = accidents["accidentType"].unique()
            # converts from numpy.ndarray to list type
            accidentList = []
            for i in accidentTypes:
                accidentList.append(i)
            return accidentList
        
        except Error as e:
            print(e)
            
        
        # """Generate and return a list of accident types in the database"""
        # # find distinct accident type values in the database
        # # return list
        # pass

    def matchAccidentType(self):
        """Find a match with keyword and return the matched Accident type as string"""
        word = self.Accident_Type_Keyword
        types = self.listAccidentType()
        
        for i in types:
            r.search(word, i)
            
        if word in types:
            return True
        else:
            return "Accident keyword not valid"
        
        # find a match (maybe use re module for regular expression)
        # pass

    
    def hourly_average(self):
        """Calculates the average number of accidents in each hour from the search result and return data for generating a plot"""
        result = self.getResult()
        #calculates number of days
        dayResult = self.getTotalDays()
        days = dayResult[0]
        hourList = []
        hourlyAccidentDict = dict()   
        #iterates through accidentTime column from result and appends to hourList 
        for row in result:
            hourList.append(row[2])
        # appends hour from hourList as key in hourlyAccidentDict and increments +1 per associated record in hourList 
        for time in hourList:
            hourlyAccidentDict[time[:2]] = hourlyAccidentDict.get(time[:2], 0) + 1
        #converts dictionary into sorted list
        hourlyAvg = []
        for key, val in hourlyAccidentDict.items():
            sort = (key, val)
            hourlyAvg.append(sort)
        sortedHourlyAvg = sorted(hourlyAvg)
        sortedAccidentList = []
        for key in sortedHourlyAvg:
            sortedAccidentList.append((key[0], key[1]/days))
        result = sorted(sortedAccidentList)
        return result
        
        # Extract ACCIDENT_TIME into (maybe) list

        #  Create dic and go through the list
        # extract only hour (first two number) and add to the dict using hour as key and value += 1

        # (maybe) convert the dict to tuple for plot module
        # return the data
    
    def accident_type(self):
        """Calculate the number of accidents in each accident type."""
        connection = connection()
        #checks if accident type is valid
        cur = connection.cursor()
        sql = "SELECT accidentType, COUNT(*) FROM Accident GROUP BY accidentType ORDER BY COUNT(*) DESC WHERE accidentType LIKE ? AND accidentDate BETWEEN ? AND ?;"
        data = (self.Accident_Type_Keyword, self.To_Date, self.From_Date)
        cur.execute(sql, data)
        result = cur.fetchall()
        return result
            # accidents = pd.read_sql(sql, connection)
            
            # # Needs to query with criteria in search object: self
            # # Use dummy search object within the function and test by print
            # return accidents
    
    def calculate_by_month():
        """Calculates the number of accidents in each month."""
        
        connection = connection()
        accidents_each_month = pd.read_sql("SELECT EXTRACT(YEAR FROM accidentDate) AS Year, EXTRACT(MONTH FROM accidentDate) AS Month FROM Accident;", connection)
        return accidents_each_month
        # Needs to use criteria in search object: self
    
    def calculate_by_day(self):
        """Calculates the number of accidents in each day."""
        connection = connection()
        cur = connection.cursor()
        sql = "SELECT dayOfWeek, COUNT(*) FROM Accident GROUP BY dayOfWeek ORDER BY COUNT(*) DESC WHERE accidentDate BEWTEEN ? AND ?;"
        data = (self.To_Date, self.From_Date)
        cur.execute(sql, data)  
        result = cur.fetchall()
        # by_day = pd.read_sql(sql, connection)
        return result
        # Needs to use criteria in search object: self

    def calculateLGA(self):
        """alculates the number of accidents in each LGA"""
        connection = connection()
        cur = connection.cursor()
        sql = "SELECT lgaName, COUNT(*) FROM Accident GROUP BY lgaName ORDER BY COUNT(*) DESC WHERE lgaName LIKE ? AND accidentDate BETWEEN ? AND ?;"
        data = (self.Lga, self.To_Date, self.From_Date)
        cur.execute(sql, data)
        result = cur.fetchall()
        return result
        # LGA = pd.read_sql("SELECT lgaName, COUNT(*) FROM Accident GROUP BY lgaName ORDER BY COUNT(*) DESC ;", connection)
        # return LGA
        # Needs to use criteria in search object: self
    
    def calculate_region():
        """Calculates the number of accidents in each region."""
        connection = connection()
        region = pd.read_sql("SELECT regionName, COUNT(*) FROM Accident GROUP BY regionName ORDER BY COUNT(*) DESC ;", connection)
        return region
        # Needs to use criteria in search object: self
        
x = Search(To_Date = "2013-08-23", From_Date = "2013-07-01")
# x.getResult()
x.hourly_average()
# print(x.getTotalDays())
# print(x)

# print(x)

# y = ["18:00", "19:00", "20:00"]
# print(y[0:2])