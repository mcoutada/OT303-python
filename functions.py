from datetime import datetime, timedelta
import os
import pandas as pd
from sqlalchemy import create_engine
from config import LOG_NAME
from logger import set_logger
from DB_connection import get_engine, db_connection
import logging

# Logs configuration 
log_name= LOG_NAME + datetime.today().strftime('%Y-%m-%d')
logger=set_logger(name_logger=log_name)

universidad = "u_de_palermo"

def extract():
    """Get data from universities. TASK OT303-45
    """    
    engine = get_engine()
    db_connection()
    logger.info('Getting data.')
                
    query = open(f"SQL/{universidad}.sql", 'r').read()
    df = pd.read_sql(query, engine)
    df.to_csv(f"files/{universidad}.csv", index=False)
    logger.info(f"Extraction complete of {universidad}")

    return df

def normalization():
    """Normalize data. TASK 
           
    """
    df = pd.read_csv(f"files/{universidad}.csv")    

    logger.info('Transforming data.')    
    # University
    df['university'] = df['university'].str.lower()
    df['university'] = df['university'].replace("_" ," " , regex = True).str.strip()

    # Career
    df['career'] = df['career'].str.lower()
    df['career'] = df['career'].replace("_" ," " , regex = True).str.strip()

    # Inscription Date.
    
    df['inscription_date'] = pd.to_datetime(df['inscription_date'])
    df['inscription_date'] = df['inscription_date'].dt.strftime('%Y-%m-%d')

    # First name.
    df['first_name'] = df['first_name'].str.lower()
    df['first_name'] = df['first_name'].replace("_" ," " , regex = True).str.strip()

    # Last name.
    df['last_name'] = df['last_name'].str.lower()
    df['last_name'] = df['last_name'].replace("_" ," " , regex = True).str.strip()

    # Gender.
    df['gender'] = df['gender'].replace(['f', 'm'], ['female', 'male'])

    # Age. 
    df['age'] = df['age'].astype(int)

    # Postal code.
    df['postal_code'] = df['postal_code'].astype('str')

    # Location.
    df['location'] = df['location'].str.lower()
    df['location'] = df['location'].replace("_" ," " , regex = True).str.strip()

    # Email.
    df['email'] = df['email'].str.lower()
    df['email'] = df['email'].str.strip()

    logger.info('Normalized Dataframe .')

    return df.to_csv(f"files/{universidad}.txt")        

def load():
    """
    Load data to S3.
    """    

if __name__ == '__main__':
    extract()
    normalization()