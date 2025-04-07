import os
import sys
from six.moves import urllib
import zipfile
from book_recommender.logger.log import logging
from book_recommender.app_exception.app_exception import AppException
from book_recommender.app_config.app_config import AppConfiguration


class DataIngestion:

    def __init__(self, app_config=AppConfiguration()):
        """
        Initialize DataIngestion class with configuration.

        Input:
        - app_config: instance of AppConfiguration (default: AppConfiguration())

        Output: None
        """
        try:
            logging.info(f"{'='*20} Starting data ingestion process. {'='*20}")
            self.data_ingestion_config = app_config.get_data_ingestion_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def download_data(self):
        """
        Downloads dataset from a given URL and saves it locally.

        Input: None
        Output:
        - zip_file_path: str, local path to the downloaded zip file
        """
        try:
            source_url = self.data_ingestion_config.dataset_download_url
            target_dir = self.data_ingestion_config.raw_data_dir

            os.makedirs(target_dir, exist_ok=True)

            file_name = os.path.basename(source_url)
            destination_path = os.path.join(target_dir, file_name)

            logging.info(f"Initiating download from: {source_url}")
            urllib.request.urlretrieve(source_url, destination_path)
            logging.info(f"File downloaded successfully at: {destination_path}")

            return destination_path

        except Exception as e:
            raise AppException(e, sys) from e

    def extract_zip_file(self, zip_file_path: str):
        """
        Unzips the provided zip file into the specified directory.

        Input:
        - zip_file_path: str, path to the downloaded zip file

        Output: None
        """
        try:
            extract_to_dir = self.data_ingestion_config.ingested_dir
            os.makedirs(extract_to_dir, exist_ok=True)

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to_dir)

            logging.info(f"Extracted contents of {zip_file_path} into {extract_to_dir}")
        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_data_ingestion(self):
        """
        Initiates the complete data ingestion process: download and extract.

        Input: None
        Output: None
        """
        try:
            downloaded_zip = self.download_data()
            self.extract_zip_file(zip_file_path=downloaded_zip)
            logging.info(f"{'='*20} Data ingestion process completed. {'='*20}\n")
        except Exception as e:
            raise AppException(e, sys) from e
