
from .base import session

async def db_add(data):
    async with session() as db_session:
        async with db_session.begin():
            db_session.add(data)
            await db_session.commit()

async def get_all(data):
    return data.scalars().all()

async def get_first(data):
    return data.scalars().first()