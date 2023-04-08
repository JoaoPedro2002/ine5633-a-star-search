import logging

VERBOSE = 25

class CustomFormatter(logging.Formatter):

    purple = "\033[95m"
    cyan = "\033[96m"
    blue = "\033[94m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: purple + format + reset,
        logging.INFO: cyan + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
        VERBOSE: blue + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logging.addLevelName(VERBOSE, "VERBOSE")
logger = logging.getLogger("Application")

ch = logging.StreamHandler()

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)

def set_level(level: str | int):
    logger.setLevel(level)
    ch.setLevel(level)