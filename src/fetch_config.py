import logging
import os
import yaml
import sys



def get_fun(conf, path_var,type):
    path = conf.get(type, {}).get(path_var)
    if path is None:
        logging.error(f"{path_var} not found in config under 'path'.")
    return path

def load_config(config_file: str,var,type):
    config_file = os.path.join('D:\\PythonProject2\\End2EndML\\src\\', 'config', config_file)
    with open(config_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        if config is None:
            logging.error(f"error occurred in config file [{config_file}]")

    if var and type:
        return get_fun(config,var,type)
    else:
        logging.error("Both input var are None.")
        return None


class GetConfig:
    def __init__(self, conf,var=None,type=None):
        self.conf = conf
        self.var = var
        self.type = type
        self.output = load_config(conf,var,type)
    def get(self):
       return self.output

