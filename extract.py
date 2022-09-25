from datetime import datetime, timedelta
import os
import pandas as pd
from sqlalchemy import create_engine
from logger import set_logger
from DB_connection import get_engine

# Logs configuration 
log_name= "Extraccion " 
logger=set_logger(name_logger=log_name)

def extract(universidad):

        logger.info('Obteniendo datos.')
        engine = get_engine()        
        query = open(f"SQL/{universidad}.sql", 'r').read()
        df = pd.read_sql(query, engine)
        df.to_csv(f"files/{universidad}.csv", index=False)
        logger.info(f"Extraccion finalizada de {universidad}")

if __name__ == '__main__':
    extract("u_de_palermo")