import time
from datetime import datetime
from sqlalchemy import create_engine, exc, inspect
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, LOG_NAME
from logger import set_logger
from decouple import config

# Logs configuration 
log_name= LOG_NAME + datetime.today().strftime('%Y-%m-%d')
logger=set_logger(name_logger=log_name)


def get_engine():
    """
    Se crea el engine de la base de datos.
    """
    url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)

def db_connection():
    """
    Conect to DB. Try 5 times, if fail cancel connection. TASK 
    """
    retry_flag = True
    retry_count = 0
    while retry_flag and retry_count <5:
        try:
            engine = get_engine()
            engine.connect()
            insp = inspect(engine)
            logger.info('Establishing connection to the database.')
            
            #check if the tables exist, if not try connecting again

            if insp.has_table("jujuy_utn") and insp.has_table("palermo_tres_de_febrero"):
                logger.info("The connection to the database has been established.")
                retry_flag=False
            else:
                retry_count = retry_count + 1
                time.sleep(60)   
        except exc.SQLAlchemyError:
                logger.info('The connection to the database could not be established.')
                retry_count=retry_count+1
                time.sleep(60)    

if __name__ == '__main__':
    db_connection()