
import logging
import time
from config.cfg import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, VILLA_MARIA, FLORES, LOCALIDAD, LOG_DB
from sqlalchemy import create_engine, inspect, exc
from datetime import datetime

# Use log created before.
log_name = LOG_DB + datetime.today().strftime('%Y-%m-%d')
logger = logging.getLogger(log_name)


def create_engine_connection():
    """Create engine for database connection.

    Returns:
        _engine.Engine: Engine
    """
    DB_CONNSTR = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
        DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
    return create_engine(DB_CONNSTR)


# Connection db no retorna el engine porque no es serializable el objeto Engine.
# Con lo cual esta funcion chequea la conexion, y para utilizar el engine se llama
# a la funcion create_engine_connection().
def connection_db():
    """Connect to Postgres database. If fail, retry up to 5 times.
    """
    retry = 0
    flag = True
    logger.info('Trying to connect to the database...')
    while flag and retry < 5:
        try:
            # Create engine to connect
            engine = create_engine_connection()
            engine.connect()
            logger.info('Connected to database.')
            insp = inspect(engine)
            # Check if tables exists.
            if insp.has_table(VILLA_MARIA) and insp.has_table(FLORES) and insp.has_table(LOCALIDAD):
                flag = False
            else:
                logger.info('Connection failed. Please wait 30 secs.')
                retry += 1
                time.sleep(30)
        except exc.SQLAlchemyError:
            # Increase error count
            retry += 1
            # Wait some seconds to try again
            logger.info('Connection failed. Please wait 30 secs.')
            time.sleep(30)
    logger.info('Connection task finished.')
    # Clear Handlers.
    logger.handlers.clear()
