import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, validator

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_DB_PATH = (ROOT_DIR / "college_rag.db").as_posix()

class Settings(BaseSettings):
    PROJECT_NAME: str = "College RAG Assistant"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = Field(default=f"sqlite:///{DEFAULT_DB_PATH}", env="DATABASE_URL")
    SUPABASE_URL: str = Field(default="", env="SUPABASE_URL")
    SUPABASE_SERVICE_ROLE_KEY: str = Field(default="", env="SUPABASE_SERVICE_ROLE_KEY")
    
    # LLM & Embeddings
    LLM_API_KEY: str = Field(default="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", env="LLM_API_KEY")
    EMBEDDING_API_KEY: str = Field(default="", env="EMBEDDING_API_KEY")
    LLM_MODEL: str = Field(default="nvidia/nemotron-3-ultra-550b-a55b", env="LLM_MODEL")
    LLM_BASE_URL: str = Field(default="https://integrate.api.nvidia.com/v1", env="LLM_BASE_URL")
    EMBEDDING_MODEL: str = Field(default="text-embedding-3-small", env="EMBEDDING_MODEL")
    
    # Security
    JWT_SECRET: str = Field(default="college_rag_assistant_super_secret_jwt_key_2026", env="JWT_SECRET")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=10080, env="ACCESS_TOKEN_EXPIRE_MINUTES") # 7 days
    
    # CORS
    CORS_ORIGINS: str = Field(default="http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173", env="CORS_ORIGINS")
    
    # RAG Parameters
    TOP_K: int = Field(default=5, env="TOP_K")
    SIMILARITY_THRESHOLD: float = Field(default=0.35, env="SIMILARITY_THRESHOLD")
    CHUNK_SIZE: int = Field(default=1000, env="CHUNK_SIZE")
    CHUNK_OVERLAP: int = Field(default=150, env="CHUNK_OVERLAP")
    MAX_HISTORY_MESSAGES: int = Field(default=6, env="MAX_HISTORY_MESSAGES")
    
    # Storage
    UPLOAD_DIR: str = "uploads"

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
if not settings.DATABASE_URL or settings.DATABASE_URL.strip() == "":
    settings.DATABASE_URL = f"sqlite:///{DEFAULT_DB_PATH}"
