
import pytest
import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3
import wx 

from accidents import hourly_average, accident_type, calculate_by_month, calculate_by_day, calculate_region, calculateLGA
#from app.main import ChartFrame, MainFrame, connect, dataRowsCount
#from app.queries import searchDateRange, searchKeyword
#from importData import getAccidentTypes, getDateRange, validateFile, importData, createDatabase, insertData
#from queries import searchKeyword, searchDateRange
#from main import connect, dataRowsCount
#from main import MainFrame

#UNIT TESTS

#ACCIDENTS.PY 

#Calculates the average number of accidents in each hour of the day.
#def test_hourly_average():
    #utput = hourly_average
    #assert output == hourly_average

"""
#Calculate the number of accidents in each accident type.
def test_accident_type():
    output = accident_type
    assert output == accident_type


#Calculates the number of accidents in each month.
def test_calculate_by_month():
    output = calculate_by_month
    assert output == calculate_by_month

#Calculates the number of accidents in each day 
def test_calculate_by_day():
    output = calculate_by_day
    assert output == calculate_by_day

#Calculates the number of accidents per region.
def test_calculate_region():
    output = calculate_region
    assert output == calculate_region

#Calculates the number of accidents per Local Government Area
def test_calculateLGA():
    output = calculateLGA
    assert output == calculateLGA


#IMPORTDATA.PY

def test_validateFile():
    output = validateFile(1)
    assert output != "validation error"

def test_importData():
    output = importData(1)
    assert output == "CSV file not valid"

def test_createDatabase():
    output = createDatabase(1)
    assert output == Error

def test_insertData():
    output = insertData(1)
    assert output == Error

def test_getDateRange():
    output = getDateRange
    assert output == getDateRange

def test_getAccidentTypes():
    output = getAccidentTypes
    assert output == getAccidentTypes



#QUERIES.PY

#def test_searchDateRange():
    #output = searchDateRange
    #assert output == searchDateRange

#def test_searchKeyword():
    #output = searchKeyword
    #assert output == searchKeyword

#MAIN.PY

#def test_connect():
    #output = connect
    #assert output == connect

#def test_dataRowsCount():
    #output = dataRowsCount
    #assert output == dataRowsCount

#def test_connect():
    #output = connect
    #assert output == connect

#MAINFRAME CLASS

#def test___init__():
    #mf = MainFrame()
    #assert mf.__init__(1) == 1
    # Is this something you test?

#def test_initialise(self):
    #mf = MainFrame()
    #assert mf.initialise(1) == 1

#def test_updateData(self):
    #mf = MainFrame()
    #assert mf.updateData(1) == 1

#def test_buildMain(self):
    #mf = MainFrame()
    #assert mf.buildMain(1) == 1

#def test_makeMenuBox(self):
    #mf = MainFrame()
    #assert mf.makeMenuBox(1) == 1

#def test_makeSearchBox(self):
    #mf = MainFrame()
    #assert mf.makeSearchBox(1) == 1

#def test_makeSumBox(self):
   #mf = MainFrame()
    #assert mf.makeSumBox(1) == 1

#def test_makeSchBar(self):
    #mf = MainFrame()
    #assert mf.makeSchbar(1) == 1

#def test_makeGridBox(self):
    #mf = MainFrame()
    #assert mf.makeGridBox(1) == 1

#def test_makeBtmBox(self):
    #mf = MainFrame()
    #assert mf.makeBtmBox(1) == 1

#def test_onFileOpen(self):
    #mf = MainFrame()
    #assert mf.onFileOpen(1) == 1

#def test_loadFile(self):
    #mf = MainFrame()
    #assert mf.loadFile(1) == 1

#def test_importBox(self):
    #mf = MainFrame()
    #assert mf.importBox(1) == 1

#def test_onDataset(self):
    #mf = MainFrame()
    #assert mf.onDataset(1) == 1

#def test_onAnalyse(self):
   #mf = MainFrame()
    #assert mf.onAnalyse(1) == 1

#def test_onAlcohol(self):
    #mf = MainFrame()
    #assert mf.onAlcohol(1) == 1

#def test_onLocation(self):
    #mf = MainFrame()
    #assert mf.onLocation(1) == 1

#def test_onChartHour(self):
    #mf = MainFrame()
    #assert mf.onChartHour(1) == 1

#def test_makeMenuBar(self):
    #mf = MainFrame()
    #assert mf.makeMenuBar(1) == 1

#def test_OnExit(self):
    #mf = MainFrame()
    #assert mf.OnExit(1) == 1

#def test_OnImport(self):
    #mf = MainFrame()
    #assert mf.OnImport(1) == 1

#def test_OnAbout(self):
    #mf = MainFrame()
    #assert mf.OnAbout(1) == 1

#CHARTFRAME CLASS

#def test___init__(self):
    #cf = ChartFrame()
    #assert cf.initialise(1) == 1

"""







