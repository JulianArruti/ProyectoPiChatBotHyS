import os


class Config:
    COHERE_API_KEY = os.getenv("COHERE_API_KEY", "your_api_key_here")
    PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY", "data/processed/")