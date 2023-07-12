import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)                  # to get module name?
LOG_FILE=f"{datetime.now().strftime('%Y_%m_%d')}.log" # log per second '%Y_%m_%d__%H_%M_%S'
logs_path=os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH=os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    # format="[ %(asctime)s] #%(lineno)d %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    format="[ %(asctime)s] [%(levelname)s] %(module)s::%(funcName)s:%(lineno)d:%(message)s", level=logging.INFO
)


# if __name__=="__main__":
#     logging.info("Logging has started")