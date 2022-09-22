import logging
from datetime import datetime
from logger import set_logger

log_name= "prueba" + datetime.today().strftime('%Y-%m-%d')

logger=set_logger(name_logger=log_name)
logger.info("funciona?")