from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://clothes:local-development-only@localhost:5433/clothes"
    taxonomy_path: str = "data/taxonomy/clothing-v1.json"
    max_images_per_item: int = Field(default=5, ge=1)
