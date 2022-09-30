import logging
def logger_universidades():
    "Same logger for both Dags"
    logger = logging.getLogger("logs_univ")

    S_handler = logging.StreamHandler()
    logger.addHandler(S_handler)


    # Adding format to logger
    # Setting lvl to info
    format = logging.Formatter(
        fmt='%(asctime)s - nombre_logger - %(message)s',
        datefmt ='%Y-%m-%d')
    S_handler.setFormatter(format)        
    logger.setLevel(logging.INFO)

    return logger
    

