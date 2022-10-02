from search import Search, hourly_average, getResult
from pandas.testing import assert_frame_equal 
import unittest
import pandas as pd
from sqlite3 import Error

class TestCases(unittest.TestCase):

    def test_hourly_average(self):
        df = pd.DataFrame({
            "ACCIDENT_TIME": ["18.30.00", "16.40.00", "13.15.00"]
            })
        expected = 1 #Need function implemented to return expected. Unsure what data type is returned.

        actual = hourly_average(df)

        assert_frame_equal(expected, actual)

    def test_getResultInvalidDates(self):
        date1 = "2012-07-01"
        date2 = "2020-02-01"

        expected = Error

        actual = getResult(self)

        self.assertEqual(expected, actual)

    









    



    
    





