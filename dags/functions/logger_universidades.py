import logging
def logger_universidades():
    logging.basicConfig(
    filename="info.log",
    format='%(asctime)s - nombre_logger - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d')
    return print("Logger activo ...")