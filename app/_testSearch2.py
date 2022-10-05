from search import Search
import unittest

class TestCases(unittest.TestCase):

    def test_hourly_average(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = []
        actual = x.hourly_average()
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
    