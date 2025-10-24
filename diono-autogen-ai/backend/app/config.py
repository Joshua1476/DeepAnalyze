"""
Configuration management for DionoAutogen AI
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "DionoAutogen AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api"
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:4000"]
    
    # LLM Configuration
    LLM_MODEL: str = "mistral-7b-instruct"
    LLM_API_URL: str = "http://localhost:11434"
    LLM_API_KEY: Optional[str] = None
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 4096
    
    # Workspace
    WORKSPACE_DIR: str = "/workspace"
    MAX_WORKSPACE_SIZE_MB: int = 1000
    
    # Execution
    MAX_EXECUTION_TIME: int = 300  # seconds
    SANDBOX_MEMORY_LIMIT: str = "2g"
    SANDBOX_CPU_LIMIT: float = 2.0
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "sqlite:///./diono_autogen.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Cloud Storage
    GOOGLE_DRIVE_CREDENTIALS: Optional[str] = None
    DROPBOX_ACCESS_TOKEN: Optional[str] = None
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/diono_autogen.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_workspace_path(project_name: str) -> str:
    """Get workspace path for a project"""
    workspace = os.path.join(settings.WORKSPACE_DIR, project_name)
    os.makedirs(workspace, exist_ok=True)
    return workspace
