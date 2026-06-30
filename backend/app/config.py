from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    youtube_api_key: str
    mongodb_uri: str
    groq_api_key: str = ""
    google_client_id: str = ""
    google_client_secret: str = ""
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"

settings = Settings()
