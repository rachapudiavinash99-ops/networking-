from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./netguardian.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    JWT_SECRET: str = "supersecretjwtkey_replace_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000", "http://localhost:5173"]
    MONITORING_INTERVAL: int = 60
    
    class Config:
        env_file = ".env"

settings = Settings()
