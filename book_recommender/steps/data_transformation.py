import os
import sys
import pickle
import pandas as pd
from book_recommender.logger.log import logging
from book_recommender.app_config.app_config import AppConfiguration
from book_recommender.app_exception.app_exception import AppException


class DataTransformation:
    def __init__(self, app_config=AppConfiguration()):
        """
        Initialize DataTransformation with application configuration.

        Input:
        - app_config: AppConfiguration object

        Output: None
        """
        try:
            config = app_config
            self.data_transformation_config = config.get_data_transformation_config()
            self.data_validation_config = config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def get_data_transformer(self):
        """
        Loads cleaned data, creates a pivot matrix of book-user ratings,
        and serializes the transformed data for use in recommendations.

        Input: None
        Output: None (saves files)
        """
        try:
            # Load the cleaned CSV file
            clean_csv = self.data_transformation_config.clean_data_file_path
            if not os.path.exists(clean_csv):
                raise FileNotFoundError(f"Cleaned data file not found at {clean_csv}")

            df = pd.read_csv(clean_csv)

            # Create pivot table: rows as book titles, columns as user IDs
            book_user_matrix = pd.pivot_table(
                data=df,
                index='title',
                columns='user_id',
                values='rating',
                aggfunc='mean',
                fill_value=0
            )

            logging.info(f"Book-user matrix created with shape: {book_user_matrix.shape}")

            # Ensure transformed directory exists
            os.makedirs(self.data_transformation_config.transformed_data_dir, exist_ok=True)
            transformed_file = os.path.join(self.data_transformation_config.transformed_data_dir, "transformed_data.pkl")
            pickle.dump(book_user_matrix, open(transformed_file, 'wb'))
            logging.info(f"Transformed data saved at: {transformed_file}")

            # Prepare and save list of book titles
            book_titles = list(book_user_matrix.index)
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)

            books_list_path = os.path.join(self.data_validation_config.serialized_objects_dir, "book_names.pkl")
            with open(books_list_path, 'wb') as f:
                pickle.dump(book_titles, f)
            logging.info(f"Book names serialized at: {books_list_path}")

            # Save pivot table again in a shared pickle for inference
            pivot_path = os.path.join(self.data_validation_config.serialized_objects_dir, "book_pivot.pkl")
            with open(pivot_path, 'wb') as f:
                pickle.dump(book_user_matrix, f)
            logging.info(f"Pivot table serialized at: {pivot_path}")

        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_data_transformation(self):
        """
        Executes the full data transformation process.

        Input: None
        Output: None
        """
        try:
            logging.info(f"{'='*20} Initiating Data Transformation {'='*20}")
            self.get_data_transformer()
            logging.info(f"{'='*20} Data Transformation Completed {'='*20}\n")
        except Exception as e:
            raise AppException(e, sys) from e
