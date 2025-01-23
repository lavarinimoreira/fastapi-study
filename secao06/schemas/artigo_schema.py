from typing import Optional

from pydantic import BaseModel, HttpUrl


class ArtigoSchema(BaseModel):
    id: Optional[int] = None
    titulo: str
    descricao: str
    url_fonte: Optional[HttpUrl] = None  # Validação de URL automática
    usuario_id: Optional[int]

    class Config:
        orm_mode = True  # Permite integração com SQLAlchemy
