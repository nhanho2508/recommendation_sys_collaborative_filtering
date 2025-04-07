from book_recommender.steps.data_ingestion import DataIngestion
from book_recommender.steps.data_validation import DataValidation
from book_recommender.steps.data_transformation import DataTransformation
from book_recommender.steps.model_train import ModelTrainer
from book_recommender.logger.log import logging


class TrainingPipeline:
    def __init__(self):
        """
        Initializes all stages of the training pipeline.
        """
        self.data_ingestion = None
        self.data_validation = None
        self.data_transformation = None
        self.model_trainer = None

    def _initialize_components(self):
        """
        Initializes pipeline components.
        """
        self.data_ingestion = DataIngestion()
        self.data_validation = DataValidation()
        self.data_transformation = DataTransformation()
        self.model_trainer = ModelTrainer()

    def start_training_pipeline(self):
        """
        Executes the full training pipeline step by step.

        Input: None
        Output: None
        """
        try:
            logging.info(f"{'='*20} Initializing Training Pipeline Components {'='*20}")
            self._initialize_components()

            logging.info(">> Starting data ingestion stage...")
            self.data_ingestion.initiate_data_ingestion()

            logging.info(">> Starting data validation stage...")
            self.data_validation.initiate_data_validation()

            logging.info(">> Starting data transformation stage...")
            self.data_transformation.initiate_data_transformation()

            logging.info(">> Starting model training stage...")
            self.model_trainer.initiate_model_trainer()

            logging.info(f"{'='*20} Training Pipeline Completed Successfully {'='*20}")

        except Exception as e:
            logging.error(f"Pipeline execution failed due to: {str(e)}")
            raise e
