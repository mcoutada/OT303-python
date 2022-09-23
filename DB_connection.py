from datetime import datime, timedelta
import time
from sqlalchemy import exc, create_engine , inspect
from decouple  import config
from logger import set_logger
from config.config import *

def get_engine():
    """
    Se crea el engine de la base de datos.
    """
    url = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    return create_engine(url)


def check_db_connection():
    retry_flag = True
    retry_count = 0
    while retry_flag and retry_count < 10:
        try:
            engine = get_engine()
            engine.connect()
            insp = inspect(engine)
            log.info('Estableciendo conexion a la base de datos.')
            #se inspecciona si existen tablas, sino prueba conectar de nuevo

            if insp.has_table(jujuy_utn) and insp.has_table(palermo_tres_de_febrero) and insp.has_table(palermo_tres_de_febrero)
                log.info('Se ha establecido la conexion con la base de datos.') 
                retry_flag=False
            else:
                retry_count = retry_count + 1
                time.sleep(60)   
default_args = {
    "retries":5,
    "retry_delay":timedelta(seconds=30)
}