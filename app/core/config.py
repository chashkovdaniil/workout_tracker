from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_HOST: str = Field(default="localhost")
    DATABASE_PORT: str = Field(default="5432")
    DATABASE_USER: str = Field(default="postgres")
    DATABASE_PASSWORD: str = Field(default="postgres")
    DATABASE_NAME: str = Field(default="postgres")
    SECRET_KEY: str = Field(default="secret")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings() 