import os
import sys
import ast
import pandas as pd
import pickle
from book_recommender.logger.log import logging
from book_recommender.app_config.app_config import AppConfiguration
from book_recommender.app_exception.app_exception import AppException


class DataValidation:
    def __init__(self, app_config=AppConfiguration()):
        """
        Initialize DataValidation with configuration settings.

        Input:
        - app_config: instance of AppConfiguration (default)

        Output: None
        """
        try:
            self.data_validation_config = app_config.get_data_validation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def preprocess_data(self):
        """
        Cleans and processes the raw books and ratings datasets.

        Input: None
        Output: None
        - Saves cleaned CSV and serialized final DataFrame as pickle
        """
        try:
            # Load ratings data
            rating_path = self.data_validation_config.ratings_csv_file
            ratings_df = pd.read_csv(rating_path, sep=";", on_bad_lines='skip', encoding='latin-1')

            # Load books data
            books_path = self.data_validation_config.books_csv_file
            books_df = pd.read_csv(books_path, sep=";", on_bad_lines='skip', encoding='latin-1')

            logging.info(f"Ratings data shape: {ratings_df.shape}")
            logging.info(f"Books data shape: {books_df.shape}")

            # Keep only relevant columns from books
            books_df = books_df[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]
            books_df.rename(columns={
                "Book-Title": "title",
                "Book-Author": "author",
                "Year-Of-Publication": "year",
                "Publisher": "publisher",
                "Image-URL-L": "image_url"
            }, inplace=True)

            # Rename columns in ratings
            ratings_df.rename(columns={
                "User-ID": "user_id",
                "Book-Rating": "rating"
            }, inplace=True)

            # Filter users who have rated more than 200 books
            active_users = ratings_df['user_id'].value_counts()
            frequent_users = active_users[active_users > 200].index
            ratings_df = ratings_df[ratings_df['user_id'].isin(frequent_users)]

            # Merge books with ratings
            combined_df = ratings_df.merge(books_df, on='ISBN')

            # Count total ratings per book title
            book_rating_counts = combined_df.groupby('title')['rating'].count().reset_index()
            book_rating_counts.rename(columns={'rating': 'num_of_rating'}, inplace=True)

            # Merge rating counts back to combined data
            enriched_df = combined_df.merge(book_rating_counts, on='title')

            # Filter out books with fewer than 50 ratings
            filtered_df = enriched_df[enriched_df['num_of_rating'] >= 50]

            # Drop duplicate entries
            final_df = filtered_df.drop_duplicates(subset=['user_id', 'title'])

            logging.info(f"Final dataset shape after cleaning: {final_df.shape}")

            # Save cleaned data as CSV
            os.makedirs(self.data_validation_config.clean_data_dir, exist_ok=True)
            clean_data_path = os.path.join(self.data_validation_config.clean_data_dir, 'clean_data.csv')
            final_df.to_csv(clean_data_path, index=False)
            logging.info(f"Cleaned data saved at: {clean_data_path}")

            # Serialize final dataset for reuse in web app
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
            pickle_path = os.path.join(self.data_validation_config.serialized_objects_dir, 'final_rating.pkl')
            pickle.dump(final_df, open(pickle_path, 'wb'))
            logging.info(f"Serialized dataset saved at: {pickle_path}")

        except Exception as e:
            raise AppException(e, sys) from e

    def initiate_data_validation(self):
        """
        Starts the data validation process.

        Input: None
        Output: None
        """
        try:
            logging.info(f"{'='*20} Starting data validation process {'='*20}")
            self.preprocess_data()
            logging.info(f"{'='*20} Data validation process completed {'='*20}\n")
        except Exception as e:
            raise AppException(e, sys) from e
