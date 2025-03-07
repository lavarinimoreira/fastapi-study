from typing import List, Optional, Any
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError


from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUp, UsuarioSchemaArtigos
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso


router = APIRouter()



# GET Logado
@router.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado

# POST / Signup
@router.post('/signup',status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(
        nome=usuario.nome, 
        sobrenome=usuario.sobrenome, 
        email=usuario.email, 
        senha=gerar_hash_senha(usuario.senha), 
        eh_admin=usuario.eh_admin)
    
    async with db as session:
        # Tratamento de erro para email duplicado
        try:
            session.add(novo_usuario)
            await session.commit()

            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="O email fornecido já está cadastrado no sistema.")
    


# GET Usuarios
@router.get('/', response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios = result.scalars().unique().all()  # Correção aplicada

        return usuarios  # FastAPI converte automaticamente os modelos para os schemas

    

# GET Usuario
@router.get('/{usuario_id}', response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK) # Usuário específico: com seus artigos.
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        

# PUT Usuario
@router.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUp, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuario_up:
            if usuario.nome:
                usuario_up.nome = usuario.nome
            if usuario.sobrenome:
                usuario_up.sobrenome = usuario.sobrenome
            if usuario.email:
                usuario_up.email = usuario.email
            if usuario.eh_admin:
                usuario_up.eh_admin = usuario.eh_admin
            if usuario.senha:
                usuario_up.senha = gerar_hash_senha(usuario.senha)

            await session.commit()

            return usuario_up
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        


# DELET Usuario
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()

        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        


# POST Login - Rota para autenticação do usuário
@router.post('/login')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # Recebe os dados do formulário OAuth2
    db: AsyncSession = Depends(get_session)  # Obtém a sessão do banco de dados
):
    """
    Essa rota autentica o usuário com base no email e senha fornecidos.
    Se a autenticação for bem-sucedida, retorna um token de acesso.
    """

    # Chama a função autenticar() para verificar se o usuário existe e se a senha está correta
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    # Se a autenticação falhar (usuário não encontrado ou senha errada)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Dados de acesso incorretos.' 
        )

    # Se a autenticação for bem-sucedida, gera um token JWT para o usuário
    token = criar_token_acesso(sub=usuario.id)  # Cria um token JWT com o ID do usuário

    # Retorna o token como resposta em formato JSON
    return JSONResponse(
        content={"acess_token": token, "token_type": "bearer"},  # Token de acesso no formato OAuth2
        status_code=status.HTTP_200_OK
    )