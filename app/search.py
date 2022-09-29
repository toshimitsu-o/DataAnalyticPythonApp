"""Class defines a search"""

import sqlite3
from sqlite3 import Error

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
    
    def hourly_average(self):
        result = self.getResult(self)
        # Import 