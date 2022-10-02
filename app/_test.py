from search import Search
from pandas.testing import assert_frame_equal 
import unittest
import pandas as pd
from sqlite3 import Error
import sqlite3

class TestCases(unittest.TestCase):

    def test_hourly_average(self):
        df = pd.DataFrame({
            "ACCIDENT_TIME": ["18.30.00", "16.40.00", "13.15.00"]
            })
        expected = 1 #Need function implemented to return expected. Unsure what data type is returned.

        actual = Search.hourly_average(df)

        assert_frame_equal(expected, actual)

    def test_getResultInvalidDates(self):
        date1 = "2012-07-01"
        date2 = "2020-02-01"

        expected = Error

        actual = Search.getResult(date1, date2)

        self.assertEqual(expected, actual)

    def test_listAccidentType(self):
        df = pd.DataFrame({
            "ACCIDENT_TYPE": ["Struck Pedestrian", "Struck Pedestrian", "Struck Pedestrian", "Collision with vehicle"]
        })
        expected = ["Struck Pedestrian", "Collision with vehicle"]

        actual = Search.listAccidentType(df)

        assert_frame_equal(expected, actual)

    def test_matchAccidentType(self):
        Search.Accident_Type_Keyword = "Struck Pedestrian"
        
        expected = "Struck Pedestrian"

        actual = Search.matchAccidentType(Search.Accident_Type_Keyword)

        self.assertEqual(expected, actual)

    def test_matchAccidentType_InvalidInput(self):
        Search.Accident_Type_Keyword = "Collision with Dinosaur"
        
        expected = Error

        actual = Search.matchAccidentType(Search.Accident_Type_Keyword)

        self.assertEqual(expected, actual)

    def test_calculate_by_month(self):
        
        


    









    



    
    





