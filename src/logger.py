import logging
import os
import sys
from datetime import datetime
from src.fetch_config import GetConfig

script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]

LOG_FILE = f"{script_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
log_path = GetConfig(conf='config_path.yml', var='log', type='path').get()
os.makedirs(log_path,exist_ok=True)

LOG_FILE_PATH = os.path.join(log_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level = logging.DEBUG,
    format = f'%(asctime)s - %(levelname)s - %(message)s - {script_name} - %(lineno)d'
)

