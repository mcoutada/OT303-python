
import logging
import time
from config.cfg import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, VILLA_MARIA, FLORES, LOCALIDAD
from sqlalchemy import create_engine, inspect, exc
from datetime import datetime

# Create and configure log
today = datetime.now().date()
logging.basicConfig(
    format='%(asctime)s %(message)s',
    filemode='w',
    level='DEBUG')


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
    while flag and retry < 5:
        try:
            # Create engine to connect
            engine = create_engine_connection()
            engine.connect()
            logging.info('Connected to database.')
            insp = inspect(engine)
            # Check if tables exists.
            if insp.has_table(VILLA_MARIA) and insp.has_table(FLORES) and insp.has_table(LOCALIDAD):
                flag = False
            else:
                logging.info('Connection failed. Please wait 30 secs.')
                retry += 1
                time.sleep(30)
        except exc.SQLAlchemyError:
            # Increase error count
            retry += 1
            # Wait some seconds to try again
            logging.info('Connection failed. Please wait 30 secs.')
            time.sleep(30)
