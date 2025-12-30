from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Taskify"
    PROJECT_VERSION: str = "0.0.1"
    DB_URL: str
    
    # JWT Configuration
    JWT_SECRET_KEY: str = "{JWT_SECRET_KEY}"
    JWT_ALGORITHM: str = "{JWT_ALGORITHM}"
    JWT_EXPIRATION_MINUTES: int = "{JWT_EXPIRATION_MINUTES}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


settings = Settings()