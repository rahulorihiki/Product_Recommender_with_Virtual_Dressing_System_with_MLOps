import os
import sys
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]" # The format of the log messages, it will also mention from which module(python file) the log message is coming from due to %(module)s

log_dir = "logs" # The directory where the logs will be stored
log_filepath = os.path.join(log_dir,"running_logs.log") # The file where the logs will be stored
os.makedirs(log_dir, exist_ok=True) # Create the directory if it does not exist



logging.basicConfig(
    level= logging.INFO, # The level of the logs. It will log all the logs with level INFO or higher. The levels are DEBUG, INFO, WARNING, ERROR, CRITICAL
    format= logging_str,

    handlers=[
        logging.FileHandler(log_filepath), # Makes sure that the logs are also stored in the running_logs.log file
        logging.StreamHandler(sys.stdout) # Makes sure that the logs are continuously printed on the console
    ]
)

logger = logging.getLogger("FashionLogger") # The name of the logger