from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:password@127.0.0.1:3306/hcp_crm"
    
    # Groq API
    GROQ_API_KEY: str
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:5173"
    
    # Application
    DEBUG: bool = True
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra="ignore"


settings = Settings()
