from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'  # ✅ Corrigido espaço extra
    DB_URL: str = 'postgresql+asyncpg://dev_gabriel:university@localhost:5432/faculdade'

    class Config:
        case_sensitive = True
        
settings: Settings = Settings()
