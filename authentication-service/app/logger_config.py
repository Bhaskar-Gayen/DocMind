import logging
import sys

def setup_logger(name=__name__):
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Check if the logger already has handlers to avoid adding multiple handlers
    if not logger.handlers:
        # Create a StreamHandler that logs to sys.stdout
        console_handler = logging.StreamHandler(sys.stdout)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Attach the formatter to the handler
        console_handler.setFormatter(formatter)

        # Attach the handler to the logger
        logger.addHandler(console_handler)

    return logger
