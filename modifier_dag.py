import logging
from datetime import timedelta, datetime
from time import strftime

import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator
from replace import replacing, folder

logging.basicConfig(level=logging.DEBUG,
                    datefmt=strftime("%Y-%m-%d"),
                    format='%(asctime)s - %(name)s - %(message)s')

logger = logging.getLogger('SDR')

#  required settings to running DAG
default_args = {
                'retries': 5,
                'retry_delay': timedelta(minutes=5)
}

#  the data required for the replacing function
df = pd.read_csv(f'{folder}/csv/zip_codes.csv')

#  creating a variable to contain the zip codes
zip_codes = df['codigo_postal']

#  Calling dag
with DAG(
        'zip_code_query',
        description='Query processing',
        default_args=default_args,
        schedule_interval=timedelta(hours=1),
        start_date=datetime(2022, 3, 4)
        ) as dag:

    replace_operator = PythonOperator(task_id='replacing_query_numbers',
                                      python_callable=replacing,
                                      #  list comprehension to looping through
                                      #  the zip code data
                                      op_args=[x for x in zip_codes[:1]],
                                      dag=dag)
    # calling the function to show it in the 'airflow' graphical scheme
    [replace_operator]
