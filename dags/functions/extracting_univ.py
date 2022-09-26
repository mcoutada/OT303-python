import psycopg2
import pandas as pd

def extracting_univ(path,name):
    conn = psycopg2.connect(
        user = 'username',
        password = 'password',
        host = 'host.com',
        port = '0000',
        database = 'training'
    )

    sql_script=open(path,"r")
    sql_text=sql_script.read()
    raw_data=pd.read_sql_query(sql_text,conn)
    raw_data.to_csv(name+".csv",header=True,index=False)
