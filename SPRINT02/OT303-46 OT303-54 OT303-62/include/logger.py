import logging
import os
import sys
import time
from functools import wraps

# Set a global variable flag to set the logger's log level.
# True --> logger's level = DEBUG
# False --> logger's level = INFO
# By default it's set to False, but it can be changed when calling our main script with argument DEBUG
# Example: python main.py DEBUG

global debug_flg
debug_flg = False


def set_logger(logger_name, is_debug=debug_flg):
    """
    Sets up the logger for the file that called this function

    Args:
        logger_name (str): main logger's name.
        is_debug (bool, optional): Sets log's level to DEBUG. Defaults to False.

    Returns:
        logging.Logger: file's logger
    """

    # The path where the first file has been triggered
    # Example:
    # cd /path/to/root_folder/main.py
    # python main.py
    # --> root_abs_path = /path/to/root_folder
    root_abs_path = os.getcwd()

    # The folder to store the log files
    log_abs_path = os.path.join(root_abs_path, "logs")

    # Set the logger's name to the base project's folder name
    # Example: /path/to/root_folder/main.py --> root_folder_name = root_folder
    root_folder_name = os.path.basename(os.getcwd())

    log_file_abs_path = os.path.join(
        # TODO: Once developing is finished, switch lines to get one log file per run
        # log_abs_path, f"{root_folder_name}_{datetime.datetime.now():%Y%m%d_%H%M%S_%f}.log"
        log_abs_path,
        f"{root_folder_name}.log",
    )

    if not os.path.exists(log_abs_path):
        os.mkdir(log_abs_path)

    # Set up the logger (to avoid using the default/root logger)
    logger = logging.getLogger(logger_name)

    # Prevents duplicate log messages when passing the log into an object (class instance)
    # https://stackoverflow.com/questions/7173033/duplicate-log-output-when-using-python-logging-module
    logger.propagate = False

    # Set up the logging level (to know which messages to log)
    # Logging messages with less severe level will be ignored, higher ones will be emitted.
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
    # | Level    | Numeric value | Description                                                                                                                 |
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
    # | CRITICAL | 50            | A serious error, indicating that the program itself may be unable to continue running.                                      |
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
    # | ERROR    | 40            | Due to a more serious problem, the software has not been able to perform some function.                                     |
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
    # | WARNING  | 30            | An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). |
    # |          |               | The software is still working as expected.                                                                                  |
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
    # | INFO     | 20            | Confirmation that things are working as expected.                                                                           |
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
    # | DEBUG    | 10            | Detailed information, typically of interest only when diagnosing problems.                                                  |
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+
    # | NOTSET   | 0             | This is the initial default setting of a log when it is created.                                                            |
    # |          |               | It is not really relevant and most developers will not even take notice of this category.                                   |
    # |          |               | In many circles, it has already become nonessential. The root log is usually created with level WARNING.                    |
    # +----------+---------------+-----------------------------------------------------------------------------------------------------------------------------+

    logger.setLevel(logging.DEBUG if is_debug else logging.INFO)

    # Set up a logging format
    formatter = logging.Formatter(
        # The format I like:
        # fmt="%(asctime)s.%(msecs)03d [%(name)-20s:%(lineno)-4d] %(levelname)8s: %(message)s",
        # datefmt="%Y-%m-%d %H:%M:%S",
        # The format requested by the task:
        fmt="%(asctime)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d",
    )

    # Set up a console handler
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)

    # Add the console handler to the logger for the messages to be shown on
    # the console
    logger.handlers.clear()
    logger.addHandler(sh)

    # Set up a file handler if a file name is provided for the messages to be
    # logged to a log file
    if log_file_abs_path:
        fh = logging.FileHandler(log_file_abs_path)
        fh.setFormatter(formatter)
        # Add the file handler to the logger
        logger.addHandler(fh)

    # Modify system's excepthook function (triggered everytime our script fails)
    # so we can log the error after failure
    new_excepthook = lambda *exc_info: log_unhandled_exception(
        logger, *exc_info)
    sys.excepthook = new_excepthook

    return logger


def log_unhandled_exception(in_logger, *in_exc_info):
    exc_type, exc_value, exc_traceback = in_exc_info
    """
    When an exception is raised and uncaught, the interpreter calls sys.excepthook with three arguments:
    the exception class, exception instance, and a traceback object.
    In an interactive session this happens just before control is returned to the prompt;
    in a Python program this happens just before the program exits.
    The handling of such top-level exceptions can be customized by assigning another three-argument function to sys.excepthook.
    sys.excepthook = log_unhandled_exception

    Logging uncaught exceptions in Python
    https://stackoverflow.com/questions/6234405/logging-uncaught-exceptions-in-python/16993115#16993115

    Args:
        *exc_info is unpacked to:
        exc_type (type): Gets the type of the exception being handled (a subclass of BaseException). Example: <class 'ZeroDivisionError'>
        exc_value (error): Gets the exception instance (an instance of the exception type). Example: division by zero
        exc_traceback (traceback): Gets a traceback object which encapsulates the call stack at the point where the exception originally occurred. Example: <traceback object at 0x7f8b8b8b8b8>
    """

    # Ignore KeyboardInterrupt so a console python program can exit with Ctrl
    # + C.
    if issubclass(exc_type, KeyboardInterrupt):
        # calls default excepthook
        # sys.__excepthook__ contains the original values of excepthook
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    # Rely entirely on python's logging module for formatting the exception.
    in_logger.critical(
        "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
    )


def get_rel_path(in_file_name):
    """
    Returns the relative path of the file. E.g. /pkg/extract.py
    Args:
        in_file_name (str): __file__ (Absolute path + file name)
    Returns:
        str: relative path of the file
    """

    return os.sep + os.path.relpath(in_file_name, start=os.getcwd())


# log a function's start, end, elapsed time, and input parameters
# https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
# https://stackoverflow.com/questions/6200270/decorator-that-prints-function-call-details-parameters-names-and-effective-valu


def log_basics(p_log):
    def decorator(function):
        # wraps preserves the function's metadata (attributes such as __name__,
        # __doc__) to not get lost through nested calls
        @wraps(function)
        def wrapper(*args, **kwargs):
            p_log.info(
                f"Starting {function.__name__}() with args: {args} and kwargs: {kwargs}"
            )
            start_time = time.perf_counter()
            result = function(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            p_log.info(
                f"Ended {function.__name__}() elapsed: {total_time:.4f} seconds")
            return result

        return wrapper

    return decorator
