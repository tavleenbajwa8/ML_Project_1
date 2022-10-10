from tkinter import E
from housing.entity.config_entity import DataIngestionConfig
import sys, os
from housing.exception import HousingException
from housing.logger import logging 
from housing.entity.artifact_entity import DataIngestionArtifact
import tarfile   #to extract zip file
from six.moves import urllib #we can download data using this file 
import pandas as pd 
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit


class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20}")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise HousingException(e, sys)
    
    
    def download_housing_data(self,) -> str:
        try:
            #extracting remote url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url

            #Getting the folder location to download file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir

            #Creating folder if  tgz_download_dir doesnt exist. If it exists we will remove it and then recreate it.
            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)

            os.makedirs(tgz_download_dir, exist_ok=True)

            housing_file_name = os.path.basename(download_url) #filename from whole url

            tgz_file_path = os.path.join(tgz_download_dir, housing_file_name)

            logging.info(f"Downloading file from :[{download_url}] into :[{tgz_file_path}]")
            
            urllib.request.urlretrieve(download_url, tgz_file_path)
            
            logging.info(f"File:[{tgz_file_path}] has been downloaded successfully")
            
            return tgz_file_path


        except Exception as e:
            raise HousingException(e,sys) from e


    def extract_tgz_file(self, tgz_file_path:str):
        try:
            #We will extract out data tgz_file_path to this raw_data_dir
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir, exist_ok=True)

            logging.info(f"Extracting tgz file: [{tgz_file_path}] into dir: [{raw_data_dir}]")
            
            with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
                
                housing_tgz_file_obj.extractall(path=raw_data_dir)

            logging.info(f"Extracting completed")

        except Exception as e:
            raise HousingException(e,sys) from e


    def split_data_as_train_test(self)-> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            housing_file_path = os.path.join(raw_data_dir, file_name)

            housing_data_frame = pd.read_csv(housing_file_path)

            #Stratified split: First we are going to create category based on median house income and on that category we will split dataset into train and test

            housing_data_frame["income_cat"] = pd.cut(
                housing_data_frame["median_income"],
                bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1,2,3,4,5]
            )

            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index, test_index in split.split(housing_data_frame, housing_data_frame["income_cat"]):
                strat_train_set = housing_data_frame.loc[train_index].drop(["income_cat", axis=1])
                strat_test_set = housing_data_frame.loc[test_index].drop(["income_cat", axis=1])

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, file_name) 


            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                strat_train_set.to_csv(train_file_path, index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                strat_test_set.to_csv(test_file_path, index=False)


            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
            test_file_path=test_file_path,
            is_ingested=True,
            message=f"Data ingestion completed succesfully."
            )

            return data_ingestion_artifact

        except Exception as e:
            raise HousingException(e,sys) from e 


    #We will call the above 3 functions into initiate_data_ingestion func

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            #Whenever we download any file we will get the file location after that we need to extract it(func given above)
            tgz_file_path = self.download_housing_data
            
            self.extract_tgz_file(tgz_file_path=tgz_file_path)

            return self.split_data_as_train_test()

        except Exception as e:
            raise HousingException(e,sys) from e
