from sqlalchemy import create_engine

from decouple import config

from ..config.config import *

import logging

# SELECCIONAR = 'SELECT * FROM public.moron_nacional_pampa'

def get_engine():
    """
    Se crea el engine de la base de datos.
    """
    url = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    return create_engine(url)

def connect_db():
    """
    Esta función se conecta a la base de datos.
    """
    try:
        engine = get_engine()
        engine.connect()
        logging.info('Se ha establecido una conexion a la base de datos.')
    except:
        logging.info('No se ha podido establecer la conexion a la base de datos.')
