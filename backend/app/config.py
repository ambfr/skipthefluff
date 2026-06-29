from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    youtube_api_key: str
    mongodb_uri: str
    groq_api_key: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
