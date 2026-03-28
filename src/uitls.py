import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import dill
import sys
from src.execption import MyException
from src.logger import logging

#import loss function
from sklearn.metrics import r2_score

#for hyperparameter tuning
from sklearn.model_selection import RandomizedSearchCV

import warnings
warnings.filterwarnings('ignore')



def train_test(data,train_path,test_path):
    # train test split
    try:
        train_set, test_set = train_test_split(data, test_size=0.2)
        logging.info(f'Train and test set created')
        print(f'Train and test set created')
    except Exception as e:
        logging.error(f'Error while creating train and test set: {e}')
        raise MyException(e, sys)

    try:
        train_set.to_csv(train_path, index=False)
        test_set.to_csv(test_path, index=False)
        logging.info(
            f'Train and test set created at {train_path} and {test_path}')
        print(f'Train and test set created at {train_path} and {test_path}')
    except Exception as exc:
        logging.error(f'Error while creating train and test set: {exc}')
        raise MyException(exc, sys)


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path, 'wb') as f:
            dill.dump(obj,f)
    except Exception as e:
        logging.error(e)
        raise MyException(e,sys)



def evaluate_model(models,x_train,y_train,x_test,y_test,params):
    models_score:dict = {}
    for name,model in models.items():
        logging.info(f'Evaluating {name}')

        random = RandomizedSearchCV(estimator=model, param_distributions=params[name],n_iter=10,n_jobs=-1,cv=3)

        logging.info(f'Random search for {name} apply hyperparameters tuning')

        random.fit(x_train,y_train)
        y_train_pred = random.predict(x_train)
        y_test_pred = random.predict(x_test)

        r2_score_train = r2_score(y_train,y_train_pred)
        r2_score_test = r2_score(y_test,y_test_pred)
        logging.info(f'model {name}: Train score: {r2_score_train} and test score: {r2_score_test}')

        models_score[model]=r2_score_test
    return models_score



