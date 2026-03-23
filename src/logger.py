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

