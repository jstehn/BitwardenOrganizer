import logging
import os

def configure_logger(name, log_level=None):
    # Create a logger
    logger = logging.getLogger(name)    
    # Set the logging level
    if log_level is None:
        log_level = os.getenv('LOG_LEVEL', 'INFO')
    #logger.setLevel(logging.getLevelName(log_level.upper()))

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    #ch.setLevel(logging.getLevelName(log_level.upper()))
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)-8s - %(message)s'))
    # Add ch to logger
    logger.addHandler(ch)

    return logger