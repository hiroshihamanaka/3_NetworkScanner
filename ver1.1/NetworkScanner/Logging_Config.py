# Logging_Config.py
import logging
from logging.handlers import RotatingFileHandler
from . import Constants

def setup_logging():
    '''
    Sets up logging for the application.

    - Creates a log file that rotates when it reaches 5MB, keeping up to 5 old versions.
    - Logs are written to both the file and console.
    - Logs include time, log level, and message.
    '''
    # Log format: time - log level - message
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    # Log file path from Constants
    log_file = Constants.LOG_FILE_NAME

    # Rotating file handler: 5MB per file, keeping 5 backups
    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
    handler.setLevel(logging.DEBUG)    # Capture all logs at DEBUG level and above

    # Formatter for the log messages
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)

    # Root logger setup
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)

    # Console handler: logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

