import os
import sys
from src.fetch_config import GetConfig
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.logger import logging
from src.execption import MyException
from src.uitls import save_object

class DataTransformation_config:
    def __init__(self):
        self.preprocessor_obj_file_path = os.path.join(GetConfig(conf='config_path.yml',var='artifact',type='path').get(),GetConfig(conf='config_file.yml',var='preprocessor',type='file').get())


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformation_config()

    def get_data_transfromer_obj(self):
        try:
            num_col = ['reading_score', 'writing_score']
            non_num_col = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch',
       'test_preparation_course']

            num_pipeline = Pipeline(
                steps=[
                    ('Imputer',SimpleImputer(strategy='median')),
                     ('Scaler',StandardScaler())
                ]
            )
            catgorical_pipeline = Pipeline(
                steps=[
                    ('Imputer',SimpleImputer(strategy='most_frequent')),
                    ('OneHotEncoder',OneHotEncoder(drop='first'))
                ]
            )

            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline',num_pipeline,num_col),
                    ('cat_pipeline',catgorical_pipeline,non_num_col)
                ]
            )

            return preprocessor


        except Exception as exc:
            logging.error(exc)
            raise MyException(exc,sys)

    def initiate_pipeline(self,train_df,test_df):
        try:
            train_df = pd.read_csv(train_df)
            test_df = pd.read_csv(test_df)
            logging.info("Train  and test data loaded")

            logging.info("obtaining preprocessor object")

            target_col = 'math_score'
            input_train_feature = train_df.drop(columns=[target_col])
            target_train_feature = train_df[target_col]

            input_test_feature = test_df.drop(columns=[target_col])
            target_test_feature = test_df[target_col]

            preprocessor_obj = self.get_data_transfromer_obj()
            logging.info("preprocessor object constructed")

            logging.info(" applying preprocessor on training and testing dataframe")

            input_feature_train_arr = preprocessor_obj.fit_transform(input_train_feature)
            input_test_feature_arr = preprocessor_obj.transform(input_test_feature)

            train_arr = np.c_[input_feature_train_arr, np.array(target_train_feature)]
            test_arr = np.c_[input_test_feature_arr, np.array(target_test_feature)]

            logging.info(" preprocessor object constructed")

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as exc:
            logging.error(exc)
            raise MyException(exc,sys)



