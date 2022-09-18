import sqlite3
from sqlite3 import Error

def searchDateRange(date1, date2):
    """returns all values within accidentDatabase.db within the specified dates

    Args:
        date1 (string): starting date for daterange
        date2 (string): end date for daterange
    """
    connection = None
    try:
        connection = sqlite3.connect("accidentDatabase.db")
        c = connection.cursor()
        sql = """SELECT * FROM Accident WHERE accidentDate BETWEEN ? AND ?"""
        data = (date1, date2)
        c.execute(sql, data)  
        result = c.fetchall()
        return result
    except Error as e:
        print(e)
        
        
x = searchDateRange("2013-07-01", "2013-07-01")
print(x)

def searchKeyword(keyword):
    None