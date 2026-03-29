import sys
import os
import pandas as pd

from src.execption import MyException
from src.uitls import load_object
from src.logger import logging
from src.fetch_config import GetConfig


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path = os.path.join(GetConfig(conf='config_path.yml',var='artifact',type='path').get(),GetConfig(conf='config_file.yml',var='model',type='file').get())
            preprocessor_path = os.path.join(GetConfig(conf='config_path.yml',var='artifact',type='path').get(),GetConfig(conf='config_file.yml',var='preprocessor',type='file').get())

            model = load_object(model_path)
            preprocessor = load_object(preprocessor_path)

            scaled_data = preprocessor.transform(features)
            pred_data = model.predict(scaled_data)
            return pred_data

        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)



class CustomData:
    def __init__(self,
                 gender,race_ethnicity,parental_level_of_education,lunch,test_preparation_course,reading_score,writing_score):
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_dataframe(self):
        try:
            custom_data = {
                'gender': [self.gender],
                'race_ethnicity': [self.race_ethnicity],
                'parental_level_of_education': [self.parental_level_of_education],
                'lunch': [self.lunch],
                'test_preparation_course': [self.test_preparation_course],
                'reading_score': [self.reading_score],
                'writing_score': [self.writing_score]
            }
            return pd.DataFrame(custom_data)
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)

