import os
import yaml
import sys
from book_recommender.app_exception.app_exception import AppException


def read_yaml_file(file_path: str) -> dict:
    """
    Load and parse a YAML file, returning its contents as a Python dictionary.

    Input:
    - file_path: str → Path to the YAML file

    Output:
    - dict → Parsed content from the YAML file

    Raises:
    - AppException: if file not found or YAML parsing fails
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"YAML file not found at path: {file_path}")

        with open(file_path, mode='rb') as file_stream:
            parsed_content = yaml.safe_load(file_stream)
            return parsed_content if parsed_content is not None else {}

    except Exception as e:
        raise AppException(e, sys) from e
