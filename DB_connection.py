import time
from sqlalchemy import create_engine, exc, insp
from logger import set_logger

# Logs configuration 
log_name= "Conexion DB" + datetime.today().strftime('%Y-%m-%d')
logger=set_logger(name_logger=log_name)


def get_engine():
    """
    Se crea el engine de la base de datos.
    """
    url = "postgresql://alkymer2:Alkemy23@training-main.cghe7e6sfljt.us-east-1.rds.amazonaws.com:5432/training"
    return create_engine(url)

def check_db_connection():
    """
    Conect to DB. Try 5 times, if fail cancel connection.
    """
    retry_flag = True
    retry_count = 0
    while retry_flag and retry_count <5:
        try:
            engine = get_engine()
            engine.connect()
            insp = inspect(engine)
            log.info('Establishing connection to the database.')
            
            #check if the tables exist, if not try connecting again

            if insp.has_table(jujuy_utn) and insp.has_table(palermo_tres_de_febrero):
                log.info("The connection to the database has been established.")
                retry_flag=False
            else:
                retry_count = retry_count + 1
                time.sleep(60)   
        except exc.SQLAlchemyError:
                log.info('The connection to the database could not be established.')
                retry_count=retry_count+1
                time.sleep(60)    

    

