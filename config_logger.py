import logging
import datetime

LOG_DELIMITER = "####################"
LOG_FILE = f"/Users/oscarjuliusadserballe/cli_scripts/logs/llm_{datetime.date.today()}.log"

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create file handler and formatter

    file_handler = logging.FileHandler(
        LOG_FILE,
        mode='a'
    )
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add handler to the logger
    logger.addHandler(file_handler)
    return logger