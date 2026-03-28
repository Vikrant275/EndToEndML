import logging
import os
import yaml
import sys


def load_config(config_file: str):
    config_file = os.path.join('D:\\PythonProject2\\End2EndML\\src\\', 'config', config_file)
    with open(config_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        if config is None:
            logging.error(f"error occurred in config file [{config_file}]")
            raise Exception(f"error occurred in config file [{config_file}]")
        else:
            return config


def get_fun(config, var, type):

    if var and type:
        try:
            conf = load_config(config)
        except FileNotFoundError:
            logging.error(f"error occurred in config file [{conf}]")
            raise Exception(f"error occurred in config file [{conf}]")

        content = conf.get(type, {}).get(var)

        if content is None:
            logging.error(f"{var} not found in config under 'path'.")
            raise Exception(f"error occurred in config file [{conf}]")

        return content

    else:
        logging.error("Both input var are None.")
        raise Exception(f"Both input var are None.")


def get_params(config,models):
    content_param:dict = {}
    if models:
        try:
            conf = load_config(config)
        except FileNotFoundError:
            logging.error(f"error occurred in config file [{conf}]")
            raise Exception(f"error occurred in config file [{conf}]")
        for model in models:
            content = conf.get(model, {})
            if content is None:
                logging.error(f"error occurred in config file [{conf}] for model '{model}'.")
                raise Exception(f"error occurred in config file [{conf}] for model '{model}'.")
            else:
                content_param[model] = content

        return content_param

    else:
        logging.error(f"model not found in config file [{models}]")
        raise Exception(f"model is not defined.")



class GetConfig:
    def __init__(self, conf,var=None,type=None):
        self.conf = conf
        self.var = var
        self.type = type
        self.content = get_fun(conf,var,type)

    def get(self):
       return self.content

class GetParams:
    def __init__(self,conf,models):
        self.conf = conf
        self.model = models
        self.params = get_params(conf,self.model)

    def get(self):
        return self.params




