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

    # def  __repr__(self):
    #     print("To_Date: ", self.To_Date,
    #     "From_Date: ", self.From_Date,
    #     "Accident_Type_Keyword: ", self.Accident_Type_Keyword,
    #     "Accident_Type_List", self.Accident_Type_List,
    #     "Output_Type: ", self.Output_Type,
    #     "Lga", self.Lga,
    #     "Region", self.Region)
    
    def getDateRange(self):
        """queries accident database to get the min and max date within the search query

        Returns:
            tuple: (minDate, maxDate)
        """
    
        con = connection()
        c = con.cursor()
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
        if self.Accident_Type_List:
            accidentList = str(self.Accident_Type_List)
        else:
            accidentList = None
        if self.Accident_Type_Keyword:
            accidentType = str(self.Accident_Type_Keyword)
        else:
            accidentType = None
        if self.Lga:
            lga = str(self.Lga)
        else:
            lga = None
        if self.Region:
            region = str(self.Region)
        else:
            region = None
            
        sql = "SELECT * FROM Accident WHERE accidentDate BETWEEN ? AND ? "
        accidentSql = "AND accidentType LIKE '%' || ? || '%'"
        lgaSql = "AND lgaName LIKE '%' || ? || '%' "
        regionSql = "AND regionName LIKE '%' || ? || '%'"
        endSql = ";"
        data = [date1, date2]

        try:
            con = connection()
            cur = con.cursor()
            if accidentType or accidentList is not None:
                data.append(accidentType)
                sql += accidentSql
            elif lga is not None:
                data.append(lga)
                sql += lgaSql
            elif region is not None:
                data.append(region)
                sql+= regionSql
                     
            # print(sql+endSql)
            # print(data)
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
    
    def accidentTypeList(self, mode=None):
        """Calculates the number of accidents with accident keyword using accident_type_list

        Returns:
            list: [(accidentType, NumofAccidents), ...] 
        """
        result = self.getResult()
        accidentType = self.Accident_Type_List
        accidentNum = dict()
        alcAccidentNum = dict()
        # iterates through result and appends self.Accident_Type_Keyword as key in accidentNum dict, increments +1 per associated record in result else continues
        for row in result:
            if row[3] == accidentType:
                accidentNum[row[3]] = accidentNum.get(row[3], 0) + 1
            elif mode == "alcohol" and row[-1] == 1:
                alcAccidentNum[row[3]] = alcAccidentNum.get(row[3], 0) + 1
            else:
                continue
        # converts dictionary into a list
        accidentNumList = []
        alcAccidentNumList = []
        combinedDict = dict()
        if mode == 'alcohol':
            for d in (accidentNum, alcAccidentNum):
                for key, val in d.items():
                    combinedDict[key].append(val) 
            for key, val in combinedDict.items():
                sort = (key, val)
                alcAccidentNumList.append(sort)
                sortedAlcAccidents = sorted(alcAccidentNumList)
            return sortedAlcAccidents
        else:
            for key, val in accidentNum.items():
                sort = (key, val)
                accidentNumList.append(sort)
            return accidentNumList
        
            
    
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
        alcHourList = []
        hourlyAccidentDict = dict()   
        alcHourlyAccidentDict = dict()
        #iterates through accidentTime column from result and appends to hourList 
        for row in result:
            hourList.append(row[2])
            if mode == 'alcohol' and row[-1] == 1:
                alcHourList.append(row[2])
        # appends hour from hourList as key in hourlyAccidentDict and increments +1 per associated record in hourList 
        for time in hourList:
            hourlyAccidentDict[time[:2]] = hourlyAccidentDict.get(time[:2], 0) + 1
        if mode == 'alcohol':
            for time in alcHourList:
                alcHourlyAccidentDict[time[:2]] = alcHourlyAccidentDict.get(time[:2], 0) + 1
        #converts dictionary into sorted list
        hourlyAvg = []
        alcHourlyAvg = []
        combinedDict = dict()
        if mode == 'alcohol':
            for d in (hourlyAccidentDict, alcHourlyAccidentDict):
                for key, val in d.items():
                    combinedDict[key].append(val) 
            for key, val in combinedDict.items():
                sort = (key, val)
                alcHourlyAvg.append(sort)
                sortedAlcHourlyAvg = sorted(alcHourlyAvg)
                sortedAlcAccidentList = []
            for key in sortedAlcHourlyAvg:
                sortedAlcAccidentList.append((key[0], key[1]/days))
                result = sorted(sortedAlcAccidentList)
                return result
        else:
            for key, val in hourlyAccidentDict.items():
                sort = (key, val)
                hourlyAvg.append(sort)
            sortedHourlyAvg = sorted(hourlyAvg)
            sortedAccidentList = []
            for key in sortedHourlyAvg:
                sortedAccidentList.append((key[0], key[1]/days))
            # if mode == 'alcohol':
            #     result = 
            result = sorted(sortedAccidentList)
            return result

    
    def calcAllAccidentType(self, mode=None):
        """calculates nnumber of accidents of all accident types

        Returns:
            list: [(accidentType, numofAccidents), ...]
        """
        result = self.getResult()
        accidentDict = dict()
        alcAccidentDict = dict() 
        for row in result:
            #iterates through result and ignores row if day of week column == None
            if row[3] == None:
                continue
            # if mode = alcohol
            if mode == 'alcohol' and row[-1] == 1:
                accidentDict[row[3]] = accidentDict.get(row[3], 0) + 1
            #iterates through result and appends day of week as key in dailyAccidentDict and increments +1 per associated record in result
            else:
                alcAccidentDict[row[3]] = alcAccidentDict.get(row[3], 0) + 1
        accidentList = []
        alcAccidentList = []
        combinedDict = dict()
        # converts dailyAccidentDict into an ordered list
        if mode == 'alcohol':
            for d in (accidentDict, alcAccidentDict):
                for key, val in d.items():
                    combinedDict[key].append(val) 
            for key, val in combinedDict.items():
                sort = (key, val)
                alcAccidentList.append(sort)
                sortedAlcAccidents = sorted(alcAccidentList)
            return sortedAlcAccidents
        else:
            for key, val in accidentDict.items():
                sort = (key, val)
                accidentList.append(sort)
            return accidentList
    
    def accident_type(self, mode=None):
        """Calculates the number of accidents with accident keyword

        Returns:
            list: [(accidentType, NumofAccidents), ...] 
        """
        result = self.getResult()
        accidentType = self.matchAccidentType()
        accidentNum = dict()
        alcAccidentNum = dict()
        # iterates through result and appends self.Accident_Type_Keyword as key in accidentNum dict, increments +1 per associated record in result else continues
        for row in result:
            if row[3] in accidentType:
                accidentNum[row[3]] = accidentNum.get(row[3], 0) + 1
            elif mode == "alcohol" and row[-1] == 1:
                alcAccidentNum[row[3]] = alcAccidentNum.get(row[3], 0) + 1
            else:
                continue
        # converts dictionary into a list
        accidentNumList = []
        alcAccidentNumList = []
        combinedDict = dict()
        if mode == 'alcohol':
            for d in (accidentNum, alcAccidentNum):
                for key, val in d.items():
                    combinedDict[key].append(val) 
            for key, val in combinedDict.items():
                sort = (key, val)
                alcAccidentNumList.append(sort)
                sortedAlcAccidents = sorted(alcAccidentNumList)
            return sortedAlcAccidents
        else:
            for key, val in accidentNum.items():
                sort = (key, val)
                accidentNumList.append(sort)
            return accidentNumList
    
    def calculate_by_month(self, mode=None):
        """Calculates the number of accidents in each month.

        Returns:
            list: [(month, numofAccidents),...]
        """
        result = self.getResult()
        dateList = []
        alcDateList = []
        monthlyAccidentDict = dict()
        alcMonthlyAccidentDict = dict()   
        #iterates through accidentDate column from result and appends full date to dateList 
        for row in result:
            dateList.append(row[1])
            if mode == 'alcohol' and row[-1] == 1:
                alcDateList.append(row[1])
        # appends month from dateList as key in monthlyAccidentDict and increments +1 per associated record in dateList 
        for date in dateList:
            monthlyAccidentDict[date[5:7]] = monthlyAccidentDict.get(date[5:7], 0) + 1
        if mode == "alcohol":
            for date in alcDateList:
                alcMonthlyAccidentDict[date[5:7]] = alcMonthlyAccidentDict.get(date[5:7], 0) + 1
        # converts dictionary into sorted list
        monthlyAccidentList = []
        alcMonthlyAccidentList = []
        combinedDict = dict()
        if mode == 'alcohol':
            # combines monthlyAccidentDict and alcMonthlyAccidentDict into 1 dictionary if mode= alcohol
            for d in (monthlyAccidentDict, alcMonthlyAccidentDict):
                for key, val in d.items():
                    combinedDict[key].append(val) 
            # converts combinedDict into a sorted list
            for key, val in combinedDict.items():
                sort = (key, val)
                alcMonthlyAccidentList.append(sort)
            sortedAlcMonthlyAccidentList = sorted(alcMonthlyAccidentList)
            result = sortedAlcMonthlyAccidentList
        else:
            # converts dictionary into sorted list
            for key, val in monthlyAccidentDict.items():
                sort = (key, val)
                monthlyAccidentList.append(sort)
            sortedMonthlyAccidentList = sorted(monthlyAccidentList)
            return sortedMonthlyAccidentList
    
    def calculate_by_day(self, mode=None):
        """Calculates the number of accidents in each day.

        Returns:
            list: [(dayofWeek, numofAccidents), ...]
        """
        result = self.getResult()
        dailyAccidentDict = dict() 
        alcDailyAccidentDict = dict()
        for row in result:
            #iterates through result and ignores row if day of week column == None
            if row[4] == None:
                continue
            elif mode == "alcohol" and row[-1] == 1:
                alcDailyAccidentDict[row[4]] = alcDailyAccidentDict.get(row[4], 0) + 1
            #iterates through result and appends day of week as key in dailyAccidentDict and increments +1 per associated record in result
            else:
                dailyAccidentDict[row[4]] = dailyAccidentDict.get(row[4], 0) + 1
        dailyAccidentList = []
        alcDailyAccidentList = []
        combinedDict = dict()
        # combines 2 dictionaries if mode = alcohol
        if mode == 'alcohol':
            for d in (dailyAccidentDict, alcDailyAccidentDict):
                for key, val in d.items():
                    combinedDict[key].append(val) 
            # converts combinedDict into an ordered list
            for key, val in combinedDict.items():
                sort = (key, val)
                alcDailyAccidentList.append(sort)
            day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            sortedAlcDailyAccidentList = sorted(alcDailyAccidentList, key = lambda d: day.index(d[0]))
            return sortedAlcDailyAccidentList
        else:
            # convertes dailyAccidentDict into an ordered list
            for key, val in dailyAccidentDict.items():
                sort = (key, val)
                dailyAccidentList.append(sort)
            day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            sortedDailyAccidentList = sorted(dailyAccidentList, key = lambda d: day.index(d[0]))
            return sortedDailyAccidentList
        
    def listLgas(self):
        """queries accident database and returns a list of all unique Lga names

        Returns:
            list: ['lgaName', ...]
        """
        
        try:
            con = connection()
            accidents = pd.read_sql("SELECT lgaName FROM Accident;", con)
            lgaNames = accidents["lgaName"].unique()
            # converts from numpy.ndarray to list type
            lgaNameList = []
            for i in lgaNames:
                lgaNameList.append(i)
            return lgaNameList
        
        except Error as e:
            print(e)
            
    def matchLga(self):
        """Find a match with self.keyword out of list of unique accidentTypes

        Returns:
            list: ['accidentType', ...]
        """
        result = self.getResult()
        word = self.Lga
        types = self.listLgas()
        matchedList = []
        for accident in types:
            if bool((r.search(word, accident, r.IGNORECASE))):
                matchedList.append(accident)
        return matchedList
            
            
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
        lga = self.matchLga()
        accidentNum = dict()
        # iterates through result and appends self.Lga as key in accidentNum dict, increments +1 per associated record in result else continues
        for row in result:
            if row[8] in lga:
                accidentNum[row[8]] = accidentNum.get(row[8], 0) + 1
            else:
                continue
        # converts accidentNum dict to tuple
        accidentNumList = []
        for key, val in accidentNum.items():
            sort = (key, val)
            accidentNumList.append(sort)
        return accidentNumList
    
    def listRegions(self):
        """queries accident database and returns a list of all unique region names

        Returns:
            list: ['regionName', ...]
        """
        
        try:
            con = connection()
            accidents = pd.read_sql("SELECT regionName FROM Accident;", con)
            regionNames = accidents["regionName"].unique()
            # converts from numpy.ndarray to list type
            regionNameList = []
            for i in regionNames:
                regionNameList.append(i)
            return regionNameList
        
        except Error as e:
            print(e)
            
    def matchRegions(self):
        """Find a match with self.Region out of list of unique region names

        Returns:
            list: ['regionName', ...]
        """
        result = self.getResult()
        word = self.Region
        types = self.listRegions()
        matchedList = []
        for accident in types:
            if bool((r.search(word, accident, r.IGNORECASE))):
                matchedList.append(accident)
        return matchedList
        
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
        region = self.matchRegions()
        accidentNum = dict()
        # iterates through result and appends self.Region as key in accidentNum dict, increments +1 per associated record in result else continues
        for row in result:
            if row[9] in region:
                accidentNum[row[9]] = accidentNum.get(row[9], 0) + 1
            else:
                continue
        # converts accidentNum dict to tuple
        accidentNumList = []
        for key, val in accidentNum.items():
            sort = (key, val)
            accidentNumList.append(sort)
        return accidentNumList

        
x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_Keyword="collision", Lga= "BAYSIDE", Region= 'EASTERN REGION')
# x.getResult()
y = x.hourly_average(mode='alcohol')
print(y)
# print(x.getTotalDays())
# print(x)

# print(x)

# y = ["18:00", "19:00", "20:00"]
# print(y[0:2])