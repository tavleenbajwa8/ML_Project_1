from tkinter import E
from housing.entity.config_entity import DataIngestionConfig
import sys, os
from housing.exception import HousingException
from housing.logger import logging 
from housing.entity.artifact_entity import DataIngestionArtifact
import tarfile   #to extract zip file
from six.moves import urllib #we can download data using this file 


class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20}")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise HousingException(e, sys)
    
    
    def download_housing_data(self,):
        try:
            #extracting remote url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url

            #Getting the folder location to download file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir

            os.makedirs(tgz_download_dir, exist_ok=True)
            
            housing_file_name = os.path.basename(download_url)

            tgz_file_path = os.path.join(tgz_download_dir, housing_file_name)

            logging.info(f"Downloading file from :[{download_url}] into :[{tgz_file_path}]")
            urllib.request.urlretrieve(download_url, tgz_file_path)
            logging.info(f"File:[{tgz_file_path}] has been downloaded successfully")
            return tgz_file_path


        except Exception as e:
            raise HousingException(e,sys) from e


    def extract_tgz_file(self):
        pass

    def split_data_as_train_test(self):
        pass

    #We will call the above 3 functions into initiate_data_ingestion func

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            #Whenever we download any file we will get the file location after that we need to extract it(func given above)
            tgz_file_path = self.download_housing_data
        except Exception as e:
            raise HousingException(e,sys) from e
