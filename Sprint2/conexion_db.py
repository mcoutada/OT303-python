from sqlalchemy import create_engine, exc, inspect

from config.config import DB_USER, PASSWORD, HOST, PORT, DB_NAME
from config.logger_base import log

import time

def get_engine():
    """
    Se crea el engine de la base de datos.
    """
    url = f"postgresql://{DB_USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    return create_engine(url)

def connect_db():
    """
    Esta función se conecta a la base de datos. Intenta conectarse 5 veces, si falla se cancela la conexion.
    Devuelve un elemento de conexion.
    """
    rety_flag = True
    retry_count = 0
    while rety_flag and retry_count < 5:
        try:
            engine = get_engine()
            engine.connect()
            insp = inspect(engine)
            log.info('Estableciendo conexion a la base de datos.')
            # Comprobando que existen las tablas.
            if (insp.has_table("moron_nacional_pampa") and insp.has_table("rio_cuarto_interamericana")):
                log.info('Se ha establecido la conexion con la base de datos.')
                rety_flag = False
            else:
                retry_count += 1
                time.sleep(60)
        except exc.SQLAlchemyError:
            log.info('No se ha podido establecer la conexion a la base de datos.')
            retry_count += 1
            time.sleep(60)
            
if __name__ == '__main__':
    connect_db()
    print(connect_db())
