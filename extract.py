import pandas as pd
from sqlalchemy import create_engine
from logger import set_logger
from DB_connection import get_engine

engine = get_engine() 
query = open("SQL/u_de_jujuy.sql", 'r').read()
df = pd.read_sql(query, engine)
df.to_csv("u_de_jujuy.csv", index=False)
