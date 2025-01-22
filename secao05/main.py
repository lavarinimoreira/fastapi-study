# OBS:
# Com o SQL MODELS não é necessário o diretório "schemas". 
# O MODELS é suficiente tanto para salvar em Banco de Dados quanto para transformar em JSON para a API.

from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router



app: FastAPI = FastAPI(title='Curso API - FastAPI SQL MODEL')
app.include_router(api_router, prefix=settings.API_V1_STR)



if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)