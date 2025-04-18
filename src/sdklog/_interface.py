import logging
from logging import Logger
from .colored_formatter import SdkColoredFormatter

def set_colored_logger(logger: Logger, clear_handler=True):
    fmt = SdkColoredFormatter('[%(asctime)s] %(message)s').show_name(True)
    ch = logging.StreamHandler()
    ch.setLevel(logger.level)
    ch.setFormatter(fmt)
    if clear_handler:
        logger.handlers.clear()
    logger.addHandler(ch)

def get_root_logger(level=logging.DEBUG) -> Logger:
    logger = logging.getLogger()
    logger.setLevel(level)
    return logger

def create_logger(name: str) -> Logger:
    return logging.getLogger().getChild(name)
