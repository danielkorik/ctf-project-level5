import logging

# Create a logger instance
logger = logging.getLogger(__name__)

# Remove any existing handlers associated with the logger object
if logger.hasHandlers():
    logger.handlers.clear()

# Function to set up the logger level based on environment
def setup_logger(env='dev'):
    # Determine the log level based on the environment
    log_level = logging.DEBUG if env == 'dev' else logging.WARNING

    # Set the logger level
    logger.setLevel(log_level)

    # Create a console handler with the appropriate log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

# Function to log messages conditionally based on the environment
def log_message(message, level='info'):
    if level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'error':
        logger.error(message)
    elif level == 'critical':
        logger.critical(message)
