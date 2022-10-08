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

    def checkTable(self):
        """Check if the table exist in the database and return True or False"""
        result = []
        #print(result)
        try:
            con = connection()
            c = con.cursor()
            #sql = "SELECT * FROM Accident LIMIT 1;"
            c.execute("SELECT * FROM Accident LIMIT 2;")
            result = c.fetchall()
        except:
            return False
        else:
            if len(result) == 2:
                return True
            else:
                return False
    
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
        minDate = c.fetchall()[0][0]
        c.execute(sqlmax)
        maxDate = c.fetchall()[0][0]
        return (minDate, maxDate)
    
    
    def getResult(self):
        """
        Get database records with the search criteria
        """
        # Set all search criteria to prepare sql query

        dateRange = self.getDateRange()
        minDate = dateRange[0]
        maxDate = dateRange[1]
        if self.From_Date:
            date1 = str(self.From_Date)
        else:
            date1 = minDate
        if self.To_Date:
            date2 = str(self.To_Date)
        else:
            date2 = maxDate
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
            if accidentType is not None:
                data.append(accidentType)
                sql += accidentSql
            if accidentList is not None:
                data.append(accidentList)
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
        dateRange = self.getDateRange()
        minDate = dateRange[0]
        maxDate = dateRange[1]
        if self.From_Date:
            date1 = str(self.From_Date)
        else:
            date1 = minDate
        if self.To_Date:
            date2 = str(self.To_Date)
        else:
            date2 = maxDate
        data = [date2, date1]
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
        if mode= 'alcohol
        Returns:
            list: [[(accidentType, numOfAlcoholAccidents), ...], [(accidentType, numOfAccidents), ...]]
        """
        result = self.getResult()
        accidentType = self.Accident_Type_List
        accidentNum = dict()
        alcAccidentNum = dict()
        regAccidentNum = dict()
        # iterates through result and appends self.Accident_Type_Keyword as key in accidentNum dict, increments +1 per associated record in result else continues
        for row in result:
            if row[3] == accidentType:
                accidentNum[row[3]] = accidentNum.get(row[3], 0) + 1
                if mode == "alcohol":
                    if row[-1] == 1:
                        alcAccidentNum[row[3]] = alcAccidentNum.get(row[3], 0) + 1
                    elif row[-1] == 0:
                        regAccidentNum[row[3]] = regAccidentNum.get(row[3], 0) + 1
            else:
                continue
        # converts dictionary into a list
        accidentNumList = []
        alcAccidentNumList = []
        # if mode = alcohol converts alc and nonAlc data into two lists
        if mode == 'alcohol':
            for key, val in alcAccidentNum.items():
                sort = (key, val)
                alcAccidentNumList.append(sort)
            for key, val in regAccidentNum.items():
                sort = (key, val)
                accidentNumList.append(sort)
            return [alcAccidentNumList, accidentNumList]
        else:
            for key, val in accidentNum.items():
                sort = (key, val)
                accidentNumList.append(sort)
            return accidentNumList
        
            
    
    def hourly_average(self, mode=None):
        """Calculates the average number of accidents in each hour from the search result and returns data for generating a plot

        Returns:
            list: [(hour, numofAccidents), ...]
        if mode = 'alcohol':
        Returns:
            list: [[(hour, avgAlcAccidentRate), ...][(hour, avgNonAlcAccidentRate), ...]]
        """
        result = self.getResult()
        #calculates number of days
        dayResult = self.getTotalDays()
        days = dayResult[0]
        hourList = []
        alcHourList = []
        regHourList = []
        hourlyAccidentDict = {'00': 0, '01' : 0, '02' : 0, '03' : 0, '04': 0, '05' : 0, '06' : 0, '07' : 0, '08': 0, '09' : 0, '10' : 0, '11' : 0,'12': 0, '13' : 0, '14' : 0, '15' : 0, '16': 0, '17' : 0, '18' : 0, '19' : 0, '20': 0, '21' : 0, '22' : 0, '23' : 0}   
        alcHourlyAccidentDict = {'00': 0, '01' : 0, '02' : 0, '03' : 0, '04': 0, '05' : 0, '06' : 0, '07' : 0, '08': 0, '09' : 0, '10' : 0, '11' : 0,'12': 0, '13' : 0, '14' : 0, '15' : 0, '16': 0, '17' : 0, '18' : 0, '19' : 0, '20': 0, '21' : 0, '22' : 0, '23' : 0} 
        regHourlyAccidentDict = {'00': 0, '01' : 0, '02' : 0, '03' : 0, '04': 0, '05' : 0, '06' : 0, '07' : 0, '08': 0, '09' : 0, '10' : 0, '11' : 0,'12': 0, '13' : 0, '14' : 0, '15' : 0, '16': 0, '17' : 0, '18' : 0, '19' : 0, '20': 0, '21' : 0, '22' : 0, '23' : 0} 
        #iterates through accidentTime column from result and appends to hourList 
        for row in result:
            hourList.append(row[2])
            if mode == 'alcohol':
                if row[-1] == 1:
                    alcHourList.append(row[2])
                elif row[-1] == 0:
                    regHourList.append(row[2])
        # print(hourList, sep=':     ')
        # print(alcHourList)
        # appends hour from hourList as key in hourlyAccidentDict and increments +1 per associated record in hourList 
        for time in hourList:
            hourlyAccidentDict[time[:2]] = hourlyAccidentDict.get(time[:2], 0) + 1
        if mode == 'alcohol':
            for time in alcHourList:
                alcHourlyAccidentDict[time[:2]] = alcHourlyAccidentDict.get(time[:2], 0) + 1
            for time in regHourList:
                regHourlyAccidentDict[time[:2]] = regHourlyAccidentDict.get(time[:2], 0) + 1
        #converts dictionary into sorted list
        hourlyAvg = []
        alcHourlyAvg = []
        # print(alcHourlyAccidentDict)
        # print(hourlyAccidentDict)
        if mode == 'alcohol':
            for key, val in alcHourlyAccidentDict.items():
                sort = (key, val)
                alcHourlyAvg.append(sort)
                sortedAlcHourlyAvg = sorted(alcHourlyAvg)
            sortedAlcAccidentList = []
            for key in sortedAlcHourlyAvg:
                sortedAlcAccidentList.append((key[0], key[1]/days))
            finalAlcAccidentList = sorted(sortedAlcAccidentList)
            
            for key, val in regHourlyAccidentDict.items():
                sort = (key, val)
                hourlyAvg.append(sort)
                sortedHourlyAvg = sorted(hourlyAvg)
            sortedAccidentList = []
            for key in sortedHourlyAvg:
                sortedAccidentList.append((key[0], key[1]/days))
            finalAccidentList = sorted(sortedAccidentList)
            
            return [finalAlcAccidentList, finalAccidentList] 
            
            # for d in (hourlyAccidentDict, alcHourlyAccidentDict):
            #     for key, val in d.items():
            #         combinedDict[key].append(val) 
            # for key, val in combinedDict.items():
            #     sort = (key, val)
            #     alcHourlyAvg.append(sort)
            #     sortedAlcHourlyAvg = sorted(alcHourlyAvg)
            #     sortedAlcAccidentList = []
            # for key in sortedAlcHourlyAvg:
            #     sortedAlcAccidentList.append((key[0], key[1]/days))
            #     result = sorted(sortedAlcAccidentList)
            #     return result
        else:
            for key, val in hourlyAccidentDict.items():
                sort = (key, val)
                hourlyAvg.append(sort)
            sortedHourlyAvg = sorted(hourlyAvg)
            sortedAccidentList = []
            for key in sortedHourlyAvg:
                sortedAccidentList.append((key[0], key[1]/days))
            result = sorted(sortedAccidentList)
            return result

    
    def calcAllAccidentType(self, mode=None):
        """calculates nnumber of accidents of all accident types

        Returns:
            list: [(accidentType, numofAccidents), ...]
        if mode = 'alcohol'
        Returns:
            list: [[(accidentType, numofAlcoholAccidents), ...], [(accidentType, numofNonAlcoholAccidents), ...]]
        """
        result = self.getResult()
        accidentDict = dict()
        alcAccidentDict = dict() 
        regAccidentDict = dict()
        for row in result:
            #iterates through result and ignores row if day of week column == None
            if row[3] == None:
                continue
            # if mode = alcohol
            if mode == 'alcohol':
                if row[-1] == 1:
                    accidentDict[row[3]] = accidentDict.get(row[3], 0) + 1
                elif row[-1] == 1:
                    regAccidentDict[row[3]] = regAccidentDict.get(row[3], 0) + 1
            #iterates through result and appends day of week as key in dailyAccidentDict and increments +1 per associated record in result
            else:
                alcAccidentDict[row[3]] = alcAccidentDict.get(row[3], 0) + 1
        accidentList = []
        alcAccidentList = []
        combinedDict = dict()
        # converts dailyAccidentDict into an ordered list
        if mode == 'alcohol':
            # for d in (accidentDict, alcAccidentDict):
            #     for key, val in d.items():
            #         combinedDict[key].append(val) 
            for key, val in alcAccidentDict.items():
                sort = (key, val)
                alcAccidentList.append(sort)
            for key, val in accidentDict.items():
                sort = (key, val)
                accidentList.append(sort)
            return [alcAccidentList, accidentList]
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
        regAccidentNum = dict()
        if mode == 'alcohol':
            for row in result:
                if row[3] in accidentType:
                    alcAccidentNum[row[3]] = alcAccidentNum.get(row[3], 0)
                    regAccidentNum[row[3]] = regAccidentNum.get(row[3], 0)
        # iterates through result and appends self.Accident_Type_Keyword as key in accidentNum dict, increments +1 per associated record in result else continues
        for row in result:
            if row[3] in accidentType:
                accidentNum[row[3]] = accidentNum.get(row[3], 0) + 1
            if mode == "alcohol" and row[3] in accidentType:
                if row[-1] == 1:
                    alcAccidentNum[row[3]] = alcAccidentNum.get(row[3], 0) + 1
                if row[-1] == 0:
                    regAccidentNum[row[3]] = regAccidentNum.get(row[3], 0) + 1
            else:
                continue
        # converts dictionary into a list
        accidentNumList = []
        alcAccidentNumList = []
        if mode == 'alcohol':
            
            for key, val in alcAccidentNum.items():
                sort = (key, val)
                alcAccidentNumList.append(sort)
                sortedAlcAccidents = sorted(alcAccidentNumList)
            
            for key, val in regAccidentNum.items():
                sort = (key, val)
                accidentNumList.append(sort)
                sortedAccidents = sorted(accidentNumList)
                
            return [sortedAlcAccidents, sortedAccidents]
            
        #     for d in (accidentNum, alcAccidentNum):
        #         for key, val in d.items():
        #             combinedDict[key].append(val) 
        #     for key, val in combinedDict.items():
        #         sort = (key, val)
        #         alcAccidentNumList.append(sort)
        #         sortedAlcAccidents = sorted(alcAccidentNumList)
        #     return sortedAlcAccidents
        
        else:
            for key, val in accidentNum.items():
                sort = (key, val)
                accidentNumList.append(sort)
            return accidentNumList
    
    def calculate_by_month(self, mode=None):
        """Calculates the number of accidents in each month.

        Returns:
            list: [(month, numofAccidents),...]
        if mode = 'alcohol'
        Returns:
            list: [[(month, numOfAlcAccidents), ...] [(month, numOfNonAlcAccidents), ...]]
        """
        result = self.getResult()
        dateList = []
        alcDateList = []
        regDateList = []
        monthlyAccidentDict = {'01' : 0, '02' : 0, '03' : 0, '04': 0, '05' : 0, '06' : 0, '07' : 0, '08': 0, '09' : 0, '10' : 0, '11' : 0,'12': 0}
        alcMonthlyAccidentDict = {'01' : 0, '02' : 0, '03' : 0, '04': 0, '05' : 0, '06' : 0, '07' : 0, '08': 0, '09' : 0, '10' : 0, '11' : 0,'12': 0}   
        regMonthlyAccidentDict = {'01' : 0, '02' : 0, '03' : 0, '04': 0, '05' : 0, '06' : 0, '07' : 0, '08': 0, '09' : 0, '10' : 0, '11' : 0,'12': 0}
        #iterates through accidentDate column from result and appends full date to dateList 
        for row in result:
            dateList.append(row[1])
            if mode == 'alcohol':
                if row[-1] == 1:
                    alcDateList.append(row[1])
                if row[-1] == 0:
                    regDateList.append(row[1])
        # appends month from dateList as key in monthlyAccidentDict and increments +1 per associated record in dateList 
        for date in dateList:
            monthlyAccidentDict[date[5:7]] = monthlyAccidentDict.get(date[5:7], 0) + 1
        if mode == "alcohol":
            for date in alcDateList:
                alcMonthlyAccidentDict[date[5:7]] = alcMonthlyAccidentDict.get(date[5:7], 0) + 1
            for date in regDateList:
                regMonthlyAccidentDict[date[5:7]] = regMonthlyAccidentDict.get(date[5:7], 0) + 1
        # converts dictionary into sorted list
        monthlyAccidentList = []
        alcMonthlyAccidentList = []
        if mode == 'alcohol':
            # combines monthlyAccidentDict and alcMonthlyAccidentDict into 1 dictionary if mode= alcohol
            for key, val in alcMonthlyAccidentDict.items():
                sort = (key, val)
                alcMonthlyAccidentList.append(sort)
            sortedAlcMonthlyAccidentList = sorted(alcMonthlyAccidentList)
            
            for key, val in regMonthlyAccidentDict.items():
                sort = (key, val)
                monthlyAccidentList.append(sort)
            sortedMonthlyAccidentList = sorted(monthlyAccidentList)
            
            return [sortedAlcMonthlyAccidentList, sortedMonthlyAccidentList]
            
            
            # for d in (monthlyAccidentDict, alcMonthlyAccidentDict):
            #     for key, val in d.items():
            #         combinedDict[key].append(val) 
            # # converts combinedDict into a sorted list
            # for key, val in combinedDict.items():
            #     sort = (key, val)
            #     alcMonthlyAccidentList.append(sort)
            # sortedAlcMonthlyAccidentList = sorted(alcMonthlyAccidentList)
            # result = sortedAlcMonthlyAccidentList
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
        dailyAccidentDict = {'Monday': 0, 'Tuesday' : 0, 'Wednesday' : 0, 'Thursday' : 0, 'Friday': 0, 'Saturday' : 0, 'Sunday' : 0} 
        alcDailyAccidentDict = {'Monday': 0, 'Tuesday' : 0, 'Wednesday' : 0, 'Thursday' : 0, 'Friday': 0, 'Saturday' : 0, 'Sunday' : 0}
        regDailyAccidentDict = {'Monday': 0, 'Tuesday' : 0, 'Wednesday' : 0, 'Thursday' : 0, 'Friday': 0, 'Saturday' : 0, 'Sunday' : 0}
        for row in result:
            #iterates through result and ignores row if day of week column == None
            if row[4] == None:
                continue
            if mode == "alcohol":
                if row[-1] == 1:
                    alcDailyAccidentDict[row[4]] = alcDailyAccidentDict.get(row[4], 0) + 1
                elif row[-1] == 0:
                    regDailyAccidentDict[row[4]] = regDailyAccidentDict.get(row[4], 0) + 1
            #iterates through result and appends day of week as key in dailyAccidentDict and increments +1 per associated record in result
            else:
                dailyAccidentDict[row[4]] = dailyAccidentDict.get(row[4], 0) + 1
        dailyAccidentList = []
        alcDailyAccidentList = []
        # combines 2 dictionaries if mode = alcohol
        if mode == 'alcohol':
            # for d in (dailyAccidentDict, alcDailyAccidentDict):
            #     for key, val in d.items():
            #         combinedDict[key].append(val) 
            # converts combinedDict into an ordered list
            for key, val in alcDailyAccidentDict.items():
                sort = (key, val)
                alcDailyAccidentList.append(sort)
            day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            sortedAlcDailyAccidentList = sorted(alcDailyAccidentList, key = lambda d: day.index(d[0]))
            
            for key, val in regDailyAccidentDict.items():
                sort = (key, val)
                dailyAccidentList.append(sort)
            day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            sortedDailyAccidentList = sorted(dailyAccidentList, key = lambda d: day.index(d[0]))
            
            return [sortedAlcDailyAccidentList, sortedDailyAccidentList]
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
            list: [(lgaName, numofAccidents), ...]
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
            list: [(regionName, numofAccidents), ...]
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

        
#x = Search(To_Date='2016-01-01', From_Date='2015-01-01', Accident_Type_Keyword='collision', Lga= "BAYSIDE", Region= 'EASTERN REGION')
#y = x.accident_type(mode = 'alcohol')
# y = x.calculate_by_day(mode = 'alcohol')
#print(y)
# print(x.getTotalDays())
# print(x)

# print(x)

# y = ["18:00", "19:00", "20:00"]
# print(y[0:2])