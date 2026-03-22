import logging
import os
import sys
from datetime import datetime

from src.execption import MyException

LOG_FILE = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
log_path = os.path.join(os.getcwd(),"logs")
os.makedirs(os.path.dirname(log_path),exist_ok=True)

LOG_FILE_PATH = os.path.join(log_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level = logging.DEBUG,
    format = '%(asctime)s - %(levelname)s - %(message)s - %(name)s - %(lineno)d'
)


if __name__ == '__main__':
    try:
        a = 10/0
    except MyException as ex:
        logging.info("divided by zero")
        raise MyException(ex,sys.exc_info()[0])
