from os import path
import re
import pandas as pd
import sqlalchemy
from db_connection import connection

#  main folder to find the required files
folder = path.abspath(path.join(path.dirname(__file__), '..'))
conn = connection()  # connection function from db_connection module


def replacing(zip_code):
    #  reading the query's file container
    with open(f'{folder}/sql/query_test.sql', "r") as fin:
        contents = fin.read()

    #  chaning it's content by using regex
    contents = re.sub(r'\b\d+\b', f'{zip_code}', contents)

    with open(f'{folder}/sql/query_test.sql', "w") as fout:
        fout.write(contents)
        query = sqlalchemy.text(contents)
        data = pd.read_sql_query(query, conn)
        print(data)
