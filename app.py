import os
import sys
import pickle
import streamlit as st
import numpy as np
from book_recommender.logger.log import logging
from book_recommender.app_config.app_config import AppConfiguration
from book_recommender.pipeline.training_pipeline import TrainingPipeline
from book_recommender.app_exception.app_exception import AppException


class Recommendation:
    def __init__(self, app_config=AppConfiguration()):
        """
        Initializes Recommendation with configuration.

        Input: 
        - app_config: AppConfiguration instance

        Output: None
        """
        try:
            self.recommendation_config = app_config.get_recommendation_config()
        except Exception as e:
            raise AppException(e, sys) from e

    def fetch_poster(self, suggestion):
        """
        Fetch image URLs for recommended books.

        Input:
        - suggestion: list of arrays with book indices

        Output:
        - List of image URLs for recommended books
        """
        try:
            image_links = []
            book_titles = []
            matched_indices = []

            pivot_data = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects, 'rb'))
            rating_data = pickle.load(open(self.recommendation_config.final_rating_serialized_objects, 'rb'))

            # Extract titles from suggested index
            for idx_array in suggestion:
                for idx in idx_array:
                    book_titles.append(pivot_data.index[idx])

            # Match titles with original dataset to get image URL
            for title in book_titles:
                matched_row = rating_data[rating_data['title'] == title].iloc[0]
                matched_indices.append(matched_row['image_url'])

            image_links.extend(matched_indices)
            return image_links

        except Exception as e:
            raise AppException(e, sys) from e

    def recommend_book(self, book_name):
        """
        Generate a list of similar books based on collaborative filtering.

        Input:
        - book_name: str

        Output:
        - Tuple[List of recommended book titles, List of poster URLs]
        """
        try:
            results = []
            model = pickle.load(open(self.recommendation_config.trained_model_path, 'rb'))
            pivot_df = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects, 'rb'))

            # Find the index of the selected book
            book_index = np.where(pivot_df.index == book_name)[0][0]

            # Perform k-NN search
            distances, indices = model.kneighbors(
                pivot_df.iloc[book_index, :].values.reshape(1, -1), n_neighbors=6
            )

            # Get poster URLs for recommended books
            posters = self.fetch_poster(indices)

            # Get book titles from index
            for array in indices:
                for idx in array:
                    results.append(pivot_df.index[idx])

            return results, posters

        except Exception as e:
            raise AppException(e, sys) from e

    def train_engine(self):
        """
        Trigger the training pipeline for the recommender system.

        Input: None
        Output: None
        """
        try:
            pipeline = TrainingPipeline()
            pipeline.start_training_pipeline()
            st.success("Training Completed Successfully!")
            logging.info("Training pipeline executed successfully.")
        except Exception as e:
            raise AppException(e, sys) from e

    def recommendations_engine(self, selected_books):
        """
        Render recommended books and posters in Streamlit UI.

        Input:
        - selected_books: str (book title selected)

        Output: Streamlit UI update
        """
        try:
            titles, posters = self.recommend_book(selected_books)
            cols = st.columns(5)

            for i in range(1, 6):
                with cols[i - 1]:
                    st.text(titles[i])
                    st.image(posters[i])

        except Exception as e:
            raise AppException(e, sys) from e


if __name__ == "__main__":
    st.set_page_config(page_title="Book Recommendation System", layout="wide")
    st.header('End-to-End Books Recommender System')
    st.markdown("A content-based and collaborative filtering recommendation engine.")

    recommender = Recommendation()

    if st.button('Train Recommender System'):
        recommender.train_engine()

    # Load book name list from pickled file
    book_list_path = os.path.join('templates', 'book_names.pkl')
    all_books = pickle.load(open(book_list_path, 'rb'))

    selected_books = st.selectbox("Choose a book you like", all_books)

    if st.button('Show Recommendations'):
        recommender.recommendations_engine(selected_books)
