import asyncio
import uuid

from sqlalchemy import select, text, func

from database import db_session
from models import  AdminModel
from models import LevelModel


async def initialize_database_data():
    async for session in db_session.get_async_session():
        levels = await session.execute(select(LevelModel))
        levels = levels.scalars().all()
        if not levels:
            await session.execute(text(
                """
                INSERT INTO level (id_l, required_points) VALUES
                (1, 0),
                (2, 50),
                (3, 200),
                (4, 400),
                (5, 750),
                (6, 1000);
                """
            ))
        admin = await session.execute(select(AdminModel))
        admin = admin.scalars().all()
        if not admin:
            await session.execute(text(
                f"""
                INSERT INTO base_user (uu_id, name, surname, email, password, is_admin) VALUES
                ('{str(uuid.uuid1())}', 'Админ', 'Админов', 'aleksey9045@gmail.com', '$2b$12$e3EPmbtAzRX6eEipyvTxaeBdyHE0MoATu8RJnymFrYY2Luh2cQPi6', true);
                """
            ))
            await session.commit()
            await session.execute(text(
                f"""
                INSERT INTO admin (id_a, base_user) VALUES
                (1, 1)
                """
            ))

asyncio.run(initialize_database_data())