import asyncio

from sqlalchemy import select, text

from database import db_session
from models import LevelModel


async def initialize_database_data():
    async for session in db_session.get_async_session():
        result = await session.execute(select(LevelModel))
        levels = result.scalars().all()
        if not levels:
            await session.execute(text(
                """
                INSERT INTO level (id_l, required_points) VALUES
                (1, 0),
                (2, 100),
                (3, 250),
                (4, 500),
                (5, 1000);
                """
            ))
            await session.commit()

asyncio.run(initialize_database_data())