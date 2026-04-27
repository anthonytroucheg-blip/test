from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    company_name: str = "Mon Entreprise"
    response_style: str = "professionnel"
    database_url: str = "sqlite:///./data/platform.db"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
