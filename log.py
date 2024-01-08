import logging

def get_log(log_file: str = 'undefined') -> logging.Logger:

    logging.getLogger().handlers = []
    logging.basicConfig(level=logging.INFO)

    log = logging.getLogger(log_file)

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
    console_handler.setFormatter(console_formatter)

    file_handler = logging.FileHandler(log_file)
    file_formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
    file_handler.setFormatter(file_formatter)

    log.addHandler(console_handler)
    log.addHandler(file_handler)

    log.info('Start Log...')

    return log