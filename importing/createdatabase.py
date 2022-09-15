
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        c = connection.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS Accident
            ([ACCIDENT_NO] STRING PRIMARY KEY,
            [ACCIDENT_DATE], STRING,
            [ACCIDENT_TIME],
            [ACCIDENT_TYPE],
            [DAY_OF_WEEK],
            [SEVERITY],
            [LONGITUDE],
            [LATITUDE],
            [LGA_NAME],
            [REGION_NAME],
            [FATALITY],
            [SERIOUSINJURY],
            [ALCOHOL_RELATED])"""
        )
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

