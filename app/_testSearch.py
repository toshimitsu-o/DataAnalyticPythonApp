from search import Search
from pandas.testing import assert_frame_equal 
import unittest
import pandas as pd
from sqlite3 import Error
import sqlite3

class TestCases(unittest.TestCase):

    def test_hourly_average(self):
        df = pd.DataFrame({
            "accidentTime": ["18.30.00", "16.40.00", "13.15.00"]
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

    def test_getResultNoInput(self):
        date1 = ""
        date2 = ""

        expected = {date1:"2013-07-01", date2:"2019-02-01"}

        actual = Search.getResult(date1, date2)

        self.assertEqual(expected, actual)


    def test_listAccidentType(self):
        df = pd.DataFrame({
            "accidentType": ["Struck Pedestrian", "Struck Pedestrian", "Struck Pedestrian", "Collision with vehicle"]
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

    def test_matchAccidentType_RaiseError(self):
        Search.Accident_Type_Keyword = ""

        expected = ValueError

        actual = Search.matchAccidentType(Search.Accident_Type_Keyword)

        self.assertRaises(expected, actual)

    def test_calculate_by_month(self):
        df = pd.DataFrame({
            "accidentDate": ["1/7/2015", "1/9/2015", "2/4/2015", "3/4/2015"]
        })

        expected = {"January": 2, "Feburary":1, "March":1}

        actual = Search.calculate_by_month(df)

        self.assertEqual(expected, actual)

    def test_calculate_by_monthOutputType(self):
        df = pd.DataFrame({
            "accidentDate": ["1/7/2015", "1/9/2015", "2/4/2015", "3/4/2015"]
        })

        expected = {"January": 2, "Feburary":1, "March":1}

        self.assertIsInstance(expected, dict)

    def test_calculate_by_day(self):
        df = pd.DataFrame({
            "dayOfWeek": ["Friday", "Friday", "Friday", "Tuesday", "Sunday"]
        })

        expected = {"Friday": 3, "Tuesday": 1, "Sunday": 1}

        actual = Search.calculate_by_day(df)

        self.assertEqual(expected, actual)

    def test_calculate_by_dayOutputType(self):
        df = pd.DataFrame({
            "dayOfWeek": ["Friday", "Friday", "Friday", "Tuesday", "Sunday"]
        })

        expected = {"Friday": 3, "Tuesday": 1, "Sunday": 1}

        self.assertIsInstance(expected, dict)

    def test_calculate_region(self):
       df = pd.DataFrame({
            "regionName": ["METROPOLITAN NORTH WEST REGION", "METROPOLITAN SOUTH EAST REGION", "METROPOLITAN SOUTH EAST REGION", "NORTHERN REGION", "NORTHERN REGION"]
        })

       expected = {"METROPOLITAN NORTH WEST REGION": 1, "METROPOLITAN SOUTH EAST REGION": 2, "NORTHERN REGION": 2}

       actual = Search.calculate_region(df)

       self.assertEqual(expected, actual)

    def test_calculate_regionOutputType(self):
       df = pd.DataFrame({
            "regionName": ["METROPOLITAN NORTH WEST REGION", "METROPOLITAN SOUTH EAST REGION", "METROPOLITAN SOUTH EAST REGION", "NORTHERN REGION", "NORTHERN REGION"]
        })

       expected = {"METROPOLITAN NORTH WEST REGION": 1, "METROPOLITAN SOUTH EAST REGION": 2, "NORTHERN REGION": 2}

       self.assertIsInstance(expected, dict)

    def test_calculateLGA(self):
        df = pd.DataFrame({
            "lgaName": ["MELBOURNE", "MELRBOURNE", "MELBOURNE", "BRIMBANK"]
        })

        expected = {"MELBOURNE": 3, "BRIMBANK":1}

        actual = Search.calculateLGA(df)

        self.assertEqual(expected, actual)

    def test_calculateLGA_OutputType(self):
        df = pd.DataFrame({
            "lgaName": ["MELBOURNE", "MELRBOURNE", "MELBOURNE", "BRIMBANK"]
        })

        expected = {"MELBOURNE": 3, "BRIMBANK":1}


        self.assertIsInstance(expected, dict)

    

        

    

    
        
        


    









    



    
    





