from utils.utils import create_folder
from config.cfg import LOGS_PATH
import logging


# Logging level:
# INFO: Confirmation that things are working as expected.
# DEBUG: Detailed information, typically of interest only when diagnosing problems.
# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
# ERROR: Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

def create_logger(name_logger, log_path):
    """Create log file.

    Args:
        name_logger (str): Name log.
        log_path (str): Path to save the log file.

    Returns:
        Logger with custom configuration.
    """
    # Create logger folder.
    create_folder(LOGS_PATH)
    # Create logger and set name.
    logger = logging.getLogger(name_logger)
    # Set log level.
    logger.setLevel(logging.INFO)
    # Create formatter.
    formatter = logging.Formatter(
        # %Y-%m-%d - nombre_logger - mensaje
        fmt='%(asctime)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d')

    # Stream Handler (for console)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File Handler (for .log)
    fh = logging.FileHandler(
        filename="{0}/{1}.log".format(log_path, name_logger),
        mode='a')  # 'a' continue, 'w' truncate.
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
