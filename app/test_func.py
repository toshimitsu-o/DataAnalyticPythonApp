from msilib.schema import Error
import pytest
import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3

from accidents import hourly_average, accident_type, calculate_by_month, calculate_by_day, calculate_region, calculateLGA
from importData import getAccidentTypes, getDateRange, validateFile, importData, createDatabase, insertData

#UNIT TESTS

#ACCIDENTS.PY 

#Calculates the average number of accidents in each hour of the day.
def test_hourly_average():
    output = hourly_average
    assert output == hourly_average

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




