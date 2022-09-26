#python file for the search class and related functions

class Search: 
    def __init__(self, To_Date, From_Date, Accident_Type_Keyword, Accident_Type_List, Output_Type, Lga, Region):
        self.To_Date = To_Date
        self.From_Date = From_Date
        self.Accident_Type_Keyword = Accident_Type_Keyword
        self.Accident_Type_List = Accident_Type_List
        self.Output_Type = Output_Type
        self.Lga = Lga
        self.Region = Region

# Uses ReGex to process accident type entered in 'Keyword'
def process_accident_type():
    pass

