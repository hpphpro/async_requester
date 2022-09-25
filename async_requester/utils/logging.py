import logging
from logging import Logger

def get_base_settings_logger(name: str):
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.INFO
    )
    logger = logging.getLogger(name)
    return logger


def info(message: str) -> Logger:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.INFO
    )
    logger = logging.getLogger()
    return logger.info(message)