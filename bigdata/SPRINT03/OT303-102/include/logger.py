import inspect
import logging
import logging.handlers
import os
import sys
import time
from functools import wraps


def set_logger(logger_name, is_debug=False):
    """
    Sets up the logger for the file that called this function.
    If it's called for the first time, it will set up the logger.
    If not, it will just return the logger all set, and just adjust
    the DEBUG flag if needed.

    Args:
        logger_name (str): main logger's name.
        is_debug (bool, optional): Sets log's level to DEBUG. Defaults to False.

    Returns:
        logging.Logger: file's logger
    """

    # Get the logger (to avoid using the default/root logger)
    logger = logging.getLogger(logger_name)

    # If it's new, then it has no handler, so we need to set it up
    if len(logger.handlers) == 0:

        # The path from where the first file has been triggered
        # Example:
        # cd /path/to/root_folder/main.py
        # python main.py
        # --> root_abs_path = /path/to/root_folder
        root_abs_path = os.getcwd()

        # The folder to store the log files
        log_abs_path = os.path.join(root_abs_path, "logs")

        # Set the logger's name to the base project's folder name
        # Example: /path/to/root_folder/main.py --> root_folder_name =
        # root_folder
        root_folder_name = os.path.basename(os.getcwd())

        log_file_abs_path = os.path.join(
            # TODO: Once developing is finished, switch lines to get one log file per run
            # log_abs_path, f"{root_folder_name}_{datetime.datetime.now():%Y%m%d_%H%M%S_%f}.log"
            log_abs_path,
            f"{root_folder_name}.log",
        )

        if not os.path.exists(log_abs_path):
            os.mkdir(log_abs_path)

        # Prevents duplicate log messages when passing the log into an object (class instance)
        # https://stackoverflow.com/questions/7173033/duplicate-log-output-when-using-python-logging-module
        logger.propagate = False

        # Set up a logging format
        formatter = logging.Formatter(
            # The format I like:
            # fmt="%(asctime)s.%(msecs)03d [%(name)-20s:%(lineno)-4d] %(levelname)8s: %(message)s",
            # datefmt="%Y-%m-%d %H:%M:%S",
            # The format requested by the task:
            fmt="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
            datefmt="%d/%m/%Y",
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
            # Set a weekly log file
            fh = logging.handlers.TimedRotatingFileHandler(filename=log_file_abs_path, when="W0")
            
            fh.setFormatter(formatter)
            # Add the file handler to the logger
            logger.addHandler(fh)

        # Modify system's excepthook function (triggered everytime our script fails)
        # so we can log the error after failure
        new_excepthook = lambda *exc_info: log_unhandled_exception(
            logger, *exc_info)
        sys.excepthook = new_excepthook

    # Set or reset the logging level (to know which messages to log)
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


"""
Decorator to log a function's start, end, elapsed time, and input parameters
https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
https://stackoverflow.com/questions/6200270/decorator-that-prints-function-call-details-parameters-names-and-effective-valu

Example:

import logger
log1 = logger.set_logger(__file__)

# In a function:
@logger.log_basics(log1)
def func1(arg1):
    return arg1 * 2

# In a class. There are other ways to do it, google "self in decorator"
# This one is pretty clear to me, even though it doesn't use the @ decorator's syntactic sugar
class Myclass1:
    def __init__(self, p_num, p_file):
        self.num = p_num
        self.log = logger.set_logger(logger_name=logger.get_rel_path(p_file))
        self.duplicate = logger.log_basics(self.log)(self.duplicate)
        self.log.info(f"Finished setting files and folders for {self.name}")
    def duplicate(self):
        return self.num * 2
"""


def log_basics(p_log):
    def decorator(func):
        # wraps preserves the function's metadata (attributes such as __name__,
        # __doc__) to not get lost through nested calls
        @wraps(func)
        def wrapper(*args, **kwargs):
            # convert arguments to a printable string
            # Example:
            # def test(a, b=4, c="blah-blah", *args, **kwargs):
            # pass
            # test(1, 2, 3, 4, 5, d=6, g=12.9)
            # >>> __main__.test ( a = 1, b = 2, c = 3, args = (4, 5), kwargs = {'d': 6, 'g': 12.9} )
            # https://stackoverflow.com/questions/6200270/decorator-that-prints-function-call-details-parameters-names-and-effective-valu
            func_args = inspect.signature(func).bind(*args, **kwargs).arguments
            func_args_str = ", ".join(
                map("{0[0]} = {0[1]!r}".format, func_args.items())
            )
            func_call_str = f"{func.__module__}.{func.__qualname__}({func_args_str})"

            p_log.info(f"Starting {func_call_str}")
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            p_log.info(
                f"Ended {func_call_str}. Elapsed: {total_time:.4f} seconds")
            return result

        return wrapper

    return decorator
