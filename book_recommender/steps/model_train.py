import os
import sys
import pickle
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from book_recommender.logger.log import logging
from book_recommender.app_config.app_config import AppConfiguration
from book_recommender.app_exception.app_exception import AppException


class ModelTrainer:
    def __init__(self, app_config=AppConfiguration()):
        """
        Initialize the ModelTrainer class with configuration.

        Input:
        - app_config: instance of AppConfiguration (default)

        Output: None
        """
        try:
            self.model_trainer_config = app_config.get_model_trainer_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def train(self):
        """
        Train the recommendation model using Nearest Neighbors algorithm.

        Input: None
        Output: None
        - Loads pivot matrix, fits model, and saves trained model as pickle.
        """
        try:
            pivot_path = self.model_trainer_config.transformed_data_file_dir

            if not os.path.exists(pivot_path):
                raise FileNotFoundError(f"Pivot file not found at: {pivot_path}")

            # Load the transformed pivot matrix
            with open(pivot_path, 'rb') as f:
                pivot_matrix = pickle.load(f)

            logging.info("Pivot data loaded successfully for model training.")

            # Convert to sparse format for efficient similarity computation
            sparse_matrix = csr_matrix(pivot_matrix)

            # Train k-NN model with brute-force search
            recommender_model = NearestNeighbors(algorithm='brute')
            recommender_model.fit(sparse_matrix)

            # Prepare to save trained model
            model_dir = self.model_trainer_config.trained_model_dir
            model_path = os.path.join(model_dir, self.model_trainer_config.trained_model_name)
            os.makedirs(model_dir, exist_ok=True)

            with open(model_path, 'wb') as model_file:
                pickle.dump(recommender_model, model_file)

            logging.info(f"Trained model saved successfully at: {model_path}")

        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_model_trainer(self):
        """
        Kickstarts the model training pipeline.

        Input: None
        Output: None
        """
        try:
            logging.info(f"{'=' * 20} Starting model training {'=' * 20}")
            self.train()
            logging.info(f"{'=' * 20} Model training completed {'=' * 20}\n")
        except Exception as e:
            raise AppException(e, sys) from e
