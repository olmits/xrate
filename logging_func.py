import logging

def create_logger(file_name):

    level = logging.DEBUG
    log = logging.getLogger(__name__)

    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s: %(message)s"))

    log.setLevel(level)
    log.addHandler(file_handler)

    return log
