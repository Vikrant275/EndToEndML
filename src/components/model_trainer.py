# imports models here

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,GradientBoostingRegressor
from xgboost import XGBRegressor

import os
import sys
from src.logger import logging
from src.execption import MyException
from src.fetch_config import GetConfig

from src.uitls import evaluate_model,save_object

from dataclasses import dataclass

@dataclass
class ModelTrainerConfig:
    train_model_conf_path = os.path.join(GetConfig(conf='config_path.yml',var='artifact',type='path').get(),GetConfig(conf='config_file.yml',var='model',type='file').get())

class ModelTrainer:
    def __init__(self):
        self.train_model_config = ModelTrainerConfig()

    def initiate_model_trainer(self,train_arr,test_arr):
        try:
            logging.info("Splitting train and test data input feature")

            x_train,x_test,y_train,y_test = (
                train_arr[:,:-1],
                test_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,-1]
            )
            models = {
                "LinearRegression": LinearRegression(),
                "SVR": SVR(),
                "KNeighborsRegressor": KNeighborsRegressor(),
                "DecisionTreeRegressor": DecisionTreeRegressor(),
                "RandomForestRegressor": RandomForestRegressor(),
                "AdaBoostRegressor": AdaBoostRegressor(),
                "GradientBoostingRegressor": GradientBoostingRegressor(),
                "XGBoostRegressor": XGBRegressor()
            }

            try:
                logging.info("Training model")
                model_score = evaluate_model(models=models,x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test)
                best_model,score = max(model_score.items(), key=lambda kv: kv[1])

                logging.info(f"Best model is {best_model} with score {score}")

                if score<0.6:
                    logging.warn("No model tarin properly")
                    raise MyException("The model has not been trained yet properly",sys)

                save_object(
                    file_path=self.train_model_config.train_model_conf_path,
                    obj=best_model,
                )


            except MyException as e:
                logging.error(e)
                raise MyException(e,sys)

        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)