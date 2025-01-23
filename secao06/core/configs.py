from typing import List

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://dev_gabriel:university@localhost:5432/faculdade'
    DBBaseModel = declarative_base()

    JWT_SECRET: str = 'Ku0VtZPz9CRXg6rxo6CaNW63u-QzZkXgzqsXuE8xTN4' # NUNCA fornecer esse tipo de informação em um projeto REAL. OK?!
    """
    import secrets

    token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = 'HS256'

    # 60 minutos * 24 horas * 7 dias => 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

    
settings: Settings = Settings()