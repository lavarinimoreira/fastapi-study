from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    # o async with garante que o session.close() seja chamado 
    # automaticamente quando o contexto da sessão for encerrada.
    async with Session() as session:
        yield session