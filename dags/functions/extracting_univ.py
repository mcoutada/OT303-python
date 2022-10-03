import psycopg2
import pandas as pd
from decouple import config

def extracting_univ(path,name):
    conn = psycopg2.connect(
        user = config('DB_DATA_USERNAME'),
        password = config('DB_DATA_PASS'),
        host = config('DB_DATA_HOST'),
        port = config('DB_DATA_PORT'),
        database = config('DB_DATA_DATABASE')
    )

    sql_script=open(path,"r")
    sql_text=sql_script.read()
    raw_data=pd.read_sql_query(sql_text,conn)
    raw_data.to_csv(name+".csv",header=True,index=False)
