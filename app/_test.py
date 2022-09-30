from search import Search, connection
import pandas as pd 


def test_initial_value():
    obj_1 = Search(1, 2, 3, 4, 5, 6, 7)     
    assert obj_1.To_Date == 1
    assert obj_1.From_Date == 2
    assert obj_1.Accident_Type_Keyword == 3
    assert obj_1.Accident_Type_List == 4
    assert obj_1.Output_Type == 5
    assert obj_1.Lga == 6
    assert obj_1.Region == 7
    

def test_hourly_average(self):
    df = connection()
    dummy = ["blah", "blah", "blah"]
    s = Search()
    test = Search.hourly_average(df)
    test2 = Search.hourly_average(dummy)
    assert Search.hourly_average(df) == test
    assert Search.hourly_average(df) != test2
    





