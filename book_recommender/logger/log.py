import logging
import os
from datetime import datetime

# Define the directory where log files will be stored
LOG_DIRECTORY_NAME = "logs"
BASE_LOG_PATH = os.path.join(os.getcwd(), LOG_DIRECTORY_NAME)

# Ensure the log directory exists
os.makedirs(BASE_LOG_PATH, exist_ok=True)

# Generate a unique log filename using the current timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"log_{timestamp}.log"
full_log_path = os.path.join(BASE_LOG_PATH, log_filename)

# Configure the logging module
logging.basicConfig(
    filename=full_log_path,
    filemode="w",  # overwrite on each run
    level=logging.NOTSET,  # capture all log levels
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s"
)
