import os
import sys
from book_recommender.logger.log import logging
from book_recommender.utils.util import read_yaml_file
from book_recommender.app_exception.app_exception import AppException
from book_recommender.app_config.entity import (
    DataIngestionConfig, 
    DataValidationConfig, 
    DataTransformationConfig, 
    ModelTrainerConfig, 
    ModelRecommendationConfig
)
from book_recommender.constants import *


class AppConfiguration:
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        """
        Initialize AppConfiguration by reading the YAML config file.

        Input:
        - config_file_path: str (default path to YAML configuration)

        Output: None
        """
        try:
            self.config_data = read_yaml_file(file_path=config_file_path)
        except Exception as e:
            raise AppException(e, sys) from e

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Constructs and returns DataIngestionConfig object.

        Input: None
        Output: DataIngestionConfig instance
        """
        try:
            ingestion_cfg = self.config_data['data_ingestion_config']
            artifact_cfg = self.config_data['artifacts_config']

            base_path = os.path.join(artifact_cfg['artifacts_dir'], ingestion_cfg['dataset_dir'])

            response = DataIngestionConfig(
                dataset_download_url=ingestion_cfg['dataset_download_url'],
                raw_data_dir=os.path.join(base_path, ingestion_cfg['raw_data_dir']),
                ingested_dir=os.path.join(base_path, ingestion_cfg['ingested_dir'])
            )

            logging.info(f"Data Ingestion Configuration: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e

    def get_data_validation_config(self) -> DataValidationConfig:
        """
        Constructs and returns DataValidationConfig object.

        Input: None
        Output: DataValidationConfig instance
        """
        try:
            validation_cfg = self.config_data['data_validation_config']
            ingestion_cfg = self.config_data['data_ingestion_config']
            artifact_cfg = self.config_data['artifacts_config']

            dataset_path = os.path.join(artifact_cfg['artifacts_dir'], ingestion_cfg['dataset_dir'])
            ingested_path = os.path.join(dataset_path, ingestion_cfg['ingested_dir'])

            response = DataValidationConfig(
                books_csv_file=os.path.join(ingested_path, validation_cfg['books_csv_file']),
                ratings_csv_file=os.path.join(ingested_path, validation_cfg['ratings_csv_file']),
                clean_data_dir=os.path.join(dataset_path, validation_cfg['clean_data_dir']),
                serialized_objects_dir=os.path.join(artifact_cfg['artifacts_dir'], validation_cfg['serialized_objects_dir'])
            )

            logging.info(f"Data Validation Configuration: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e

    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        Constructs and returns DataTransformationConfig object.

        Input: None
        Output: DataTransformationConfig instance
        """
        try:
            transform_cfg = self.config_data['data_transformation_config']
            validation_cfg = self.config_data['data_validation_config']
            ingestion_cfg = self.config_data['data_ingestion_config']
            artifact_cfg = self.config_data['artifacts_config']

            dataset_root = os.path.join(artifact_cfg['artifacts_dir'], ingestion_cfg['dataset_dir'])

            response = DataTransformationConfig(
                clean_data_file_path=os.path.join(dataset_root, validation_cfg['clean_data_dir'], 'clean_data.csv'),
                transformed_data_dir=os.path.join(dataset_root, transform_cfg['transformed_data_dir'])
            )

            logging.info(f"Data Transformation Configuration: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        """
        Constructs and returns ModelTrainerConfig object.

        Input: None
        Output: ModelTrainerConfig instance
        """
        try:
            trainer_cfg = self.config_data['model_trainer_config']
            transform_cfg = self.config_data['data_transformation_config']
            ingestion_cfg = self.config_data['data_ingestion_config']
            artifact_cfg = self.config_data['artifacts_config']

            transformed_file = os.path.join(
                artifact_cfg['artifacts_dir'],
                ingestion_cfg['dataset_dir'],
                transform_cfg['transformed_data_dir'],
                'transformed_data.pkl'
            )

            model_output_dir = os.path.join(artifact_cfg['artifacts_dir'], trainer_cfg['trained_model_dir'])

            response = ModelTrainerConfig(
                transformed_data_file_dir=transformed_file,
                trained_model_dir=model_output_dir,
                trained_model_name=trainer_cfg['trained_model_name']
            )

            logging.info(f"Model Trainer Configuration: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e

    def get_recommendation_config(self) -> ModelRecommendationConfig:
        """
        Constructs and returns ModelRecommendationConfig object.

        Input: None
        Output: ModelRecommendationConfig instance
        """
        try:
            recommendation_cfg = self.config_data['recommendation_config']
            trainer_cfg = self.config_data['model_trainer_config']
            validation_cfg = self.config_data['data_validation_config']
            artifact_cfg = self.config_data['artifacts_config']

            serialized_dir = os.path.join(artifact_cfg['artifacts_dir'], validation_cfg['serialized_objects_dir'])
            model_dir = os.path.join(artifact_cfg['artifacts_dir'], trainer_cfg['trained_model_dir'])

            response = ModelRecommendationConfig(
                book_name_serialized_objects=os.path.join(serialized_dir, 'book_names.pkl'),
                book_pivot_serialized_objects=os.path.join(serialized_dir, 'book_pivot.pkl'),
                final_rating_serialized_objects=os.path.join(serialized_dir, 'final_rating.pkl'),
                trained_model_path=os.path.join(model_dir, trainer_cfg['trained_model_name'])
            )

            logging.info(f"Recommendation Configuration: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e
