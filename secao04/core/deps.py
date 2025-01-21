# # Dependências da aplicação
# from typing import Generator

# from sqlalchemy.ext.asyncio import AsyncSession

# from core.database import Session


# async def get_session() -> Generator:
#     session: AsyncSession = Session()

#     try:
#         yield session
#     finally:
#         await session.close()

########################################################################
# Dependências da aplicação
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Session  # Certifique-se de que está importando corretamente

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()
