import os
import pandas as pd
import numpy as np
import dill
import sys
from src.execption import MyException
from src.logger import logging



def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path, 'wb') as f:
            dill.dump(obj,f)
    except Exception as e:
        logging.error(e)
        raise MyException(e,sys)
