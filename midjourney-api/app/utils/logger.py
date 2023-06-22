import logging
import os
from enum import Enum
from logging.handlers import TimedRotatingFileHandler


class LogLevel(Enum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40
    CRITICAL = 50


def setup_logger(
    name: str,
    level: LogLevel = LogLevel.INFO,
    debug_sql: bool = False,
) -> logging.Logger:
    logging.basicConfig(level=level.value)
    logger = logging.getLogger(name)

    logs_folder = "logs"
    os.makedirs(logs_folder, exist_ok=True)
    log_file = os.path.join(logs_folder, "logfile.log")

    handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=30
    )
    handler.suffix = "%Y-%m-%d.log"

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    if debug_sql:
        logger_db_client = logging.getLogger("db_client")
        logger_db_client.setLevel(logging.DEBUG)
        logger_db_client.addHandler(handler)

        logger_tortoise = logging.getLogger("tortoise")
        logger_tortoise.setLevel(logging.DEBUG)
        logger_tortoise.addHandler(handler)

    logger.removeHandler(handler)
    return logger
