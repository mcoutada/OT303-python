##Configurar los log para el grupo de universidades C

import logging
from datetime import datetime

def set_logger(name_logger):
    """Create logger.
    Args:
        name_logger (str): Name log.       
    Returns:
        Logger with custom configuration."""

    # Create logger
    logger = logging.getLogger(name_logger)

    # Create a Stream Handler to show logs in console
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    # Create format.
    format = logging.Formatter(
        # %Y-%m-%d - nombre_logger - mensaje
        fmt ='%(asctime)s - %(name)s - %(message)s',
        datefmt ='%Y-%m-%d')

    ch.setFormatter(format)        

    # Setting level to info 
    logger.setLevel(logging.INFO)

    return logger
