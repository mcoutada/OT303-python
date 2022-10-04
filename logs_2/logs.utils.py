from inspect import ArgSpec
from utils.utils import create_folder
from config.cfg import LOGS_PATH
import logging
import logging.config
import os
from config.myHandler import MyHandler



def create_logger(name_logger , log_path):

    ArgSpec:
    name_logger (str): 
    log_path (str):

    returns:
    logging.Logger

    create_folder(LOGS_PATH)

    logger=logging.getLogger(name_logger)

    logger.setLevel(logging.INFO)

    formatter=logging.Formatter(
        fmt='%(asctime)s_%(levelname)s_%(name)s_%(message)s',
        datefmt=Ý%-%m-%d
    )


    #para consola
    ch=logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)


    #para el log

    fh = logging.FileHandler(
        filename="{0}/{1}.log".format(log_path, name_logger),
        mode='a')  # 'a' continue, 'w' truncate.
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

def create_logger_from_file(config:str):

    logging.handlers.MyFileHandler=MyFileHandler

    log_file_path= os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'config', config
    )

    logging.config.fileConfig(log_file_path)

def get_logger(name: str) -> logging.Logger:
  
        return logging.getLogger(name)