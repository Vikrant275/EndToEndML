import pandas as pd
import os
import sys
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.execption import MyException
import logging
import src.logger
from src.fetch_config import GetConfig

#for testing purpose
from src.components.data_transformation import  DataTransformation


@dataclass  # it helps to define class self variable
class DataIngestionConfig:
    train_path:str = os.path.join(GetConfig(conf='config_path.yml', var='artifact', type='path').get(),GetConfig(conf='config_file.yml', var='train_data', type='file').get())
    test_path:str = os.path.join(GetConfig(conf='config_path.yml', var='artifact', type='path').get(),GetConfig(conf='config_file.yml', var='test_data', type='file').get())
    raw_path:str = os.path.join(GetConfig(conf='config_path.yml', var='artifact', type='path').get(),GetConfig(conf='config_file.yml', var='raw_data', type='file').get())

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig() # consist of all value from DataIngestion class to this variable


    def initiate_data_ingestion(self):  # it fun to helps read data from database
        logging.info('Initializing data_ingestion and reading data ')
        import_path = GetConfig(conf='config_path.yml', var='input_data', type='path').get()
        file_name = GetConfig(conf='config_file.yml', var='input_data', type='file').get()
        input_data = os.path.join(import_path, file_name)
        try:
            df = pd.read_csv(input_data)
            logging.info(f'Data loaded from {import_path} to dataframe')


            os.makedirs(os.path.dirname(self.ingestion_config.train_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_path,index=False,header=True)
            logging.info(f'Raw Data saved to file {self.ingestion_config.raw_path}')
            print(f'Raw Data saved to file {self.ingestion_config.raw_path}')

            # train test split
            try:
                train_set,test_set = train_test_split(df,test_size=0.2)
                logging.info(f'Train and test set created')
                print(f'Train and test set created')
            except Exception as e:
                logging.error(f'Error while creating train and test set: {e}')
                raise MyException(e,sys)

            train_set.to_csv(self.ingestion_config.train_path,index=False)
            test_set.to_csv(self.ingestion_config.test_path,index=False)
            logging.info(f'Train and test set created at {self.ingestion_config.train_path} and {self.ingestion_config.test_path}')
            print(f'Train and test set created at {self.ingestion_config.train_path} and {self.ingestion_config.test_path}')

            return(
                self.ingestion_config.train_path,
                self.ingestion_config.test_path
            )

        except Exception as e:
            raise MyException(e,sys)


if __name__=='__main__':
    config = DataIngestion()
    x_train,x_test = config.initiate_data_ingestion()

    datatransform = DataTransformation()
    datatransform.initiate_pipeline(x_train,x_test)



