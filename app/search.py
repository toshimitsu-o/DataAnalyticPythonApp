"""Class defines a search"""

import sqlite3
from sqlite3 import Error
import pandas as pd
import re as r
from collections import OrderedDict

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
        """queries accident database to get the min and max date within the search query

        Returns:
            tuple: (minDate, maxDate)
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
            list: [(numofDays,)]
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

        Returns:
            list: ['accidentType', ...]
        """
        
        try:
            con = connection()
            accidents = pd.read_sql("SELECT accidentType FROM Accident;", con)
            accidentTypes = accidents["accidentType"].unique()
            # converts from numpy.ndarray to list type
            accidentList = []
            for i in accidentTypes:
                accidentList.append(i)
            return accidentList
        
        except Error as e:
            print(e)

    def matchAccidentType(self):
        """Find a match with self.keyword out of list of unique accidentTypes

        Returns:
            list: ['accidentType', ...]
        """
        result = self.getResult()
        word = self.Accident_Type_Keyword
        types = self.listAccidentType()
        matchedList = []
        for accident in types:
            if bool((r.search(word, accident, r.IGNORECASE))):
                matchedList.append(accident)
        return matchedList
            
        
        # for keyword in types:
        #     r.match(word, keyword)
            
        # if word in types:
        #     return True
        # else:
        #     return "Accident keyword not valid"
        
        # find a match (maybe use re module for regular expression)
        # pass

    
    def hourly_average(self, mode=None):
        """Calculates the average number of accidents in each hour from the search result and returns data for generating a plot

        Returns:
            list: [(hour, numofAccidents), ...]
        """
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

    
    def calcAllAccidentType(self):
        """calculates nnumber of accidents of all accident types

        Returns:
            list: [(accidentType, numofAccidents), ...]
        """
        result = self.getResult()
        accidentDict = dict() 
        for row in result:
            #iterates through result and ignores row if day of week column == None
            if row[3] == None:
                continue
            #iterates through result and appends day of week as key in dailyAccidentDict and increments +1 per associated record in result
            else:
                accidentDict[row[3]] = accidentDict.get(row[3], 0) + 1
        accidentList = []
        # converts dailyAccidentDict into an ordered list
        for key, val in accidentDict.items():
            sort = (key, val)
            accidentList.append(sort)
        return accidentList
    
    def accident_type(self):
        """Calculates the number of accidents with accident keyword

        Returns:
            list: [(accidentType, NumofAccidents), ...] 
        """
        result = self.getResult()
        accidentType = self.matchAccidentType()
        accidentNum = dict()
        # iterates through result and appends self.Accident_Type_Keyword as key in accidentNum dict, increments +1 per associated record in result else continues
        for row in result:
            if row[3] in accidentType:
                accidentNum[row[3]] = accidentNum.get(row[3], 0) + 1
            else:
                continue
        # converts dictionary into a list
        accidentNumList = []
        for key, val in accidentNum.items():
            sort = (key, val)
            accidentNumList.append(sort)
        print(accidentNumList)
    
    def calculate_by_month(self):
        """Calculates the number of accidents in each month.

        Returns:
            list: [(month, numofAccidents),...]
        """
        result = self.getResult()
        dateList = []
        monthlyAccidentDict = dict()   
        #iterates through accidentDate column from result and appends full date to dateList 
        for row in result:
            dateList.append(row[1])
        # appends month from dateList as key in monthlyAccidentDict and increments +1 per associated record in dateList 
        for date in dateList:
            monthlyAccidentDict[date[5:7]] = monthlyAccidentDict.get(date[5:7], 0) + 1
        # converts dictionary into sorted list
        monthlyAccidentList = []
        for key, val in monthlyAccidentDict.items():
            sort = (key, val)
            monthlyAccidentList.append(sort)
        sortedMonthlyAccidentList = sorted(monthlyAccidentList)
        return sortedMonthlyAccidentList
    
    def calculate_by_day(self):
        """Calculates the number of accidents in each day.

        Returns:
            list: [(dayofWeek, numofAccidents), ...]
        """
        result = self.getResult()
        dailyAccidentDict = dict() 
        for row in result:
            #iterates through result and ignores row if day of week column == None
            if row[4] == None:
                continue
            #iterates through result and appends day of week as key in dailyAccidentDict and increments +1 per associated record in result
            else:
                dailyAccidentDict[row[4]] = dailyAccidentDict.get(row[4], 0) + 1
        dailyAccidentList = []
        # converts dailyAccidentDict into an ordered list
        for key, val in dailyAccidentDict.items():
            sort = (key, val)
            dailyAccidentList.append(sort)
        day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        sortedDailyAccidentList = sorted(dailyAccidentList, key = lambda d: day.index(d[0]))
        return sortedDailyAccidentList
        
    def calcAllLgas(self):
        """Calculates the number of accidents in each LGA

        Returns:
            list: [(lgaName, numofAccidents), ...]
        """
        result = self.getResult()
        lgaAccidentDict = dict()
        #iterates through result and appends lgaName as key in lgaAccidentDict and increments +1 per associated record in result
        for row in result:
            lgaAccidentDict[row[8]] = lgaAccidentDict.get(row[8], 0) + 1
        lgaAccidentList = []
        # converts dailyAccidentDict into a list
        for key, val in lgaAccidentDict.items():
            sort = (key, val)
            lgaAccidentList.append(sort)
        return lgaAccidentList

    def calculateLGA(self):
        """Calculates the number of accidents within a given lga

        Returns:
            tuple: (lgaName, numofAccidents)
        """
        result = self.getResult()
        lga = self.Lga
        accidentNum = dict()
        # iterates through result and appends self.Lga as key in accidentNum dict, increments +1 per associated record in result else continues
        for row in result:
            if row[8] == lga:
                accidentNum[row[8]] = accidentNum.get(row[8], 0) + 1
            else:
                continue
        # converts accidentNum dict to tuple
        accidentNumList = None
        for key, val in accidentNum.items():
            accidentNumList = (key, val)
        return accidentNumList
        
    def calcAllRegions(self):
        """Calculates the number of accidents in each region.

        Returns:
            list: [(regionName, numofAccidents), ...]
        """
        result = self.getResult()
        regionAccidentDict = dict()
        #iterates through result and appends regionName as key in regionAccidentDict and increments +1 per associated record in result
        for row in result:
            regionAccidentDict[row[9]] = regionAccidentDict.get(row[9], 0) + 1
        # print(regionAccidentDict)
        regionAccidentList = []
        # converts regionAccidentDict into a list
        for key, val in regionAccidentDict.items():
            sort = (key, val)
            regionAccidentList.append(sort)
        return regionAccidentList
    
    def calculate_region(self):
        """calculates the num of accidents within a given region

        Returns:
            tuple: (regionName, numofAccidents)
        """
        result = self.getResult()
        region = self.Region
        accidentNum = dict()
        # iterates through result and appends self.Region as key in accidentNum dict, increments +1 per associated record in result else continues
        for row in result:
            if row[9] == region:
                accidentNum[row[9]] = accidentNum.get(row[9], 0) + 1
            else:
                continue
        # converts accidentNum dict to tuple
        accidentNumList = None
        for key, val in accidentNum.items():
            accidentNumList = (key, val)
        return accidentNumList

        
x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_Keyword="collision", Lga= "BAYSIDE", Region= 'EASTERN REGION')
# x.getResult()
x.accident_type()
# print(y)
# print(x.getTotalDays())
# print(x)

# print(x)

# y = ["18:00", "19:00", "20:00"]
# print(y[0:2])