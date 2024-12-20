# La idea era importar los datos de configuracion pero me estaba dando problemas y termine llamando todo directamente en cada archivo

import os


class Config:
    COHERE_API_KEY = os.getenv("COHERE_API_KEY", "your_api_key_here")
    PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY", "data/processed/")