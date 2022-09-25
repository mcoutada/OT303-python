from datetime import datetime, timedelta
import time
from sqlalchemy import create_engine
from logger import set_logger


def get_engine():
    """
    Se crea el engine de la base de datos.
    """
    url = "postgresql://alkymer2:Alkemy23@training-main.cghe7e6sfljt.us-east-1.rds.amazonaws.com:5432/training"
    return create_engine(url)

    

