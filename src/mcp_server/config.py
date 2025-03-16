from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    model_name: str = "llama3"
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = str(Path(__file__).parent.parent.parent / ".env")

settings = Settings()