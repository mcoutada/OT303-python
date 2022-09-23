import include.logger as logger
import sys


def main(args):

    # Set the logger's log level
    logger.debug_flg = True if args[0:1] == ["DEBUG"] else False
    # Set the logger for this file
    log = logger.set_logger(logger_name=logger.get_rel_path(__file__))

    log.info("Start Main")

    a = 1 / 0


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
