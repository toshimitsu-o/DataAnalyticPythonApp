from wsgiref.validate import validator
import pandas as pd
import csv
from pycsvschema.checker import Validator
import sys
from csvvalidator import *
import datetime

def importFile(fileName):
    
    """function accepts csv file, performs schema valiation and returns a list of tuples containing relevant
    information from csv file 
    """
    # attempts to validate csv file
    try:
        # list of required fields
        schema = {
            "fields": [
                {
                    "name": "ACCIDENT_NO",
                    "required": True
                },
                {
                    "name": "ACCIDENT_DATE",
                    "required": True
                },
                {
                    "name": "ACCIDENT_TIME",
                    "required": True
                },
                {
                    "name": "ACCIDENT_TYPE",
                    "required": True
                },
                {
                    "name": "DAY_OF_WEEK",
                    "required": True
                },
                {
                    "name": "SEVERITY",
                    "required": True
                },
                {
                    "name": "LONGITUDE",
                    "required": True
                },
                {
                    "name": "LATITUDE",
                    "required": True
                },
                {
                    "name": "LGA_NAME",
                    "required": True
                },
                {
                    "name": "REGION_NAME",
                    "required": True
                },
                {
                    "name": "FATALITY",
                    "required": True
                },
                {
                    "name": "SERIOUSINJURY",
                    "required": True
                },
                {
                    "name": "ALCOHOL_RELATED",
                    "required": True
                },
            ]
        }
        # validates csv file against listed schema
        v = Validator(fileName, schema=schema)
        v.validate()
        
    # if validation fails returns this error
    except:
        return "validation error"
            
    # if validation is successful this code will execute
    else:
        wb = pd.read_csv(fileName)
        accidentData = []
        
        # iterates through each row and appends required field information as a tuple to the list accidentData
        for index, row in wb.iterrows():
            aNo = row[1]
            # converts dates from dd/mm/yyyy to yyyy-mm-dd format
            aDate = datetime.datetime.strptime(row[4], "%d/%m/%Y").strftime("%Y-%m-%d")
            # converts time from hh.mm.ss to hh:mm:ss format
            aTime = row[5]
            aFTime = None
            for i in aTime:
                if i ==".":
                    aFTime.append(":")
                else:
                    aFTime.append(i)
            print(aFTime)
            # aTime = datetime.datetime.strptime(row[5], "$HH.%mm.%ss").strftime("%H:%M:%S")
            # print(aTime)
        #     aType = row[7]
        #     dayOfWeek = row[8]
        #     severity = row[14]
        #     longitude = row[18]
        #     latitude = row[19]
        #     lgaName = row[21]
        #     regionName = row[22]
        #     fatality = row[27]
        #     seriousInjury = row[28]
        #     alcoholRelated = row[45]
        #     accidentData.append((aNo, aDate, aTime, aType, dayOfWeek, severity, longitude, latitude, lgaName, regionName, fatality, seriousInjury, alcoholRelated))
        # return accidentData
    
    
    
importFile("C:/Users/zeefe/OneDrive/Documents/Uni/Year 2/Trimester 2/Software Technologies/Git Repositories/2810ICT-2022-Assignment/2810ICT-2022-Assignment/dataset/Crash Statistics Victoria.csv")

    

    
#     field_names = ("ACCIDENT_NO",
#                 "ACCIDENT_DATE",
#                 "ACCIDENT_TIME",
#                 "ACCIDENT_TYPE",
#                 "DAY_OF_WEEK",
#                 "SEVERITY",
#                 "LONGITUDE",
#                 "LATITUDE",
#                 "LGA_NAME",
#                 "REGION_NAME",
#                 "FATALITY",
#                 "SERIOUSINJURY",
#                 "ALCOHOL_RELATED"
#     )

    # validator = CSVValidator(field_names)

    # # basic header and record length checks
    # validator.add_header_check('EX1', 'bad header')
    # validator.add_record_length_check('EX2', 'unexpected record length')

    # # # some simple value checks
    # # validator.add_value_check('ACCIDENT_NO', str,
    # #                         'EX3', 'study id must be an integer')
    # # validator.add_value_check('patient_id', int,
    # #                         'EX4', 'patient id must be an integer')
    # # validator.add_value_check('gender', enumeration('M', 'F'),
    # #                         'EX5', 'invalid gender')
    # # validator.add_value_check('age_years', number_range_inclusive(0, 120, int),
    # #                         'EX6', 'invalid age in years')
    # # validator.add_value_check('date_inclusion', datetime_string('%Y-%m-%d'),
    # #                         'EX7', 'invalid date')

    # # # a more complicated record check
    # # def check_age_variables(r):
    # #     age_years = int(r['age_years'])
    # #     age_months = int(r['age_months'])
    # #     valid = (age_months >= age_years * 12 and
    # #             age_months % age_years < 12)
    # #     if not valid:
    # #         raise RecordError('EX8', 'invalid age variables')
    # # validator.add_record_check(check_age_variables)

    # # # validate the data and write problems to stdout
    # # data = csv.reader(fileName, delimiter='\t')
    
    # problems = validator.validate(fileName)
    # write_problems(problems, sys.stdout)

# importFile("C:/Users/zeefe/OneDrive/Documents/Uni/Year 2/Trimester 2/Software Technologies/Git Repositories/2810ICT-2022-Assignment/2810ICT-2022-Assignment/dataset/Crash Statistics Victoria.csv")



# wb = Workbook()
# ws = wb.active()

# val = dv(type="list", formula1= "ACCIDENT_NO, ACCIDENT_DATE, ACCIDENT_TIME, ACCIDENT_TYPE, DAY_OF_WEEK, SEVERITY, LONGITUDE, LATITUDE, LGA_NAME, REGION_NAME, FATALITY, SERIOUSINJURY, ALCOHOL_RELATED", allow_blank=False)

# val.error = "Invalid entry in list"
# val.errorTitle = "Invalid entry"



    # field_names = ("ACCIDENT_NO",
    #             "ACCIDENT_DATE",
    #             "ACCIDENT_TIME",
    #             "ACCIDENT_TYPE",
    #             "DAY_OF_WEEK",
    #             "SEVERITY",
    #             "LONGITUDE",
    #             "LATITUDE",
    #             "LGA_NAME",
    #             "REGION_NAME",
    #             "FATALITY",
    #             "SERIOUSINJURY",
    #             "ALCOHOL_RELATED"
    # )
