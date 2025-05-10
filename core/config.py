from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    MONGO_URL: str
    SECRET_KEY:str
    PRIVATE_JWT_ALGO:str
    S3_REGION:str
    S3_ACCESS_KEY_ID:str
    S3_SECRET_ACCESS_KEY:str
    S3_BUCKET_NAME:str
    GEMINI_API_KEY:str


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
