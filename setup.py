from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## edit below variables as per your requirements -
REPO_NAME = "ML Based Books Recommender System"
AUTHOR_USER_NAME = "NHANHT"
SRC_REPO = "books_recommender"
LIST_OF_REQUIREMENTS = []


setup(
    name=SRC_REPO,
    version="0.0.1",
    author="NHANHT",
    description="Simple Books Recommendation Using Collaborative Filtering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author_email="ư",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS
)
