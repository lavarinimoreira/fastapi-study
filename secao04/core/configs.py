from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    """
    Configurações Gerais usadas na aplicação
    """
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://dev_gabriel:university@localhost:5432/faculdade'
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True

settings = Settings()