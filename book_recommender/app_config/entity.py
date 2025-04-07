from typing import NamedTuple


class DataIngestionConfig(NamedTuple):
    """
    Configuration for data ingestion process.

    Attributes:
    - dataset_download_url: str → URL to download dataset
    - raw_data_dir: str → Directory to store downloaded zip
    - ingested_dir: str → Directory to extract raw dataset
    """
    dataset_download_url: str
    raw_data_dir: str
    ingested_dir: str


class DataValidationConfig(NamedTuple):
    """
    Configuration for validating and preprocessing dataset.

    Attributes:
    - clean_data_dir: str → Path to store cleaned data CSV
    - books_csv_file: str → Path to ingested books.csv
    - ratings_csv_file: str → Path to ingested ratings.csv
    - serialized_objects_dir: str → Directory to store pickle files
    """
    clean_data_dir: str
    books_csv_file: str
    ratings_csv_file: str
    serialized_objects_dir: str


class DataTransformationConfig(NamedTuple):
    """
    Configuration for transforming data into pivot matrix.

    Attributes:
    - clean_data_file_path: str → Path to cleaned data CSV
    - transformed_data_dir: str → Path to store transformed matrix
    """
    clean_data_file_path: str
    transformed_data_dir: str


class ModelTrainerConfig(NamedTuple):
    """
    Configuration for training recommendation model.

    Attributes:
    - transformed_data_file_dir: str → Path to transformed pivot data
    - trained_model_dir: str → Directory to save trained model
    - trained_model_name: str → Name of model file to save
    """
    transformed_data_file_dir: str
    trained_model_dir: str
    trained_model_name: str


class ModelRecommendationConfig(NamedTuple):
    """
    Configuration for loading model and serialized files during inference.

    Attributes:
    - book_name_serialized_objects: str → Path to pickled book names
    - book_pivot_serialized_objects: str → Path to pickled pivot matrix
    - final_rating_serialized_objects: str → Path to pickled full rating data
    - trained_model_path: str → Path to pickled trained model
    """
    book_name_serialized_objects: str
    book_pivot_serialized_objects: str
    final_rating_serialized_objects: str
    trained_model_path: str
