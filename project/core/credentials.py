import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Webcup-2023"
    PROJECT_VERSION: str = "0.0.1"

    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_SERVER: str = os.getenv("DB_SERVER", "localhost")
    # default DB port is 5432
    DB_PORT: str = os.getenv("DB_PORT", 3306)
    DB_NAME: str = os.getenv("DB_NAME", "tdd")
    DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


settings = Settings()
