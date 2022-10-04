import logging
import logging.config

logging.config.fileConfig('../config/logger.cfg')

# Creando log desde un archivo cfg
def get_logger():
    return logging.getLogger("root")

