from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Healthcare Modernization API"
    app_version: str = "1.0.0"
    database_url: str = "postgresql://healthcare:healthcare@db:5432/healthcare"
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = {"env_prefix": "HEALTHCARE_"}


settings = Settings()
