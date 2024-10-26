from typing import Any, Dict

from sqlalchemy import insert, update, bindparam, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database import db_session
from models import BaseUserModel, UserModel, InterestsModel, LevelModel
from querys import SelectQuery, BaseQuery

Base = db_session.base

class LevelsSelectQuery(SelectQuery):
    @classmethod
    async def get_level(cls, payload: dict, session: AsyncSession) -> dict[str, Any]:
        bu_data = await SelectQuery.select(BaseUserModel.id_bu, BaseUserModel.uu_id == payload["sub"], session)
        u_data = await SelectQuery.select(UserModel.points, UserModel.base_user == int(bu_data["id_bu"]), session)
        level = await session.execute(select(LevelModel.id_l).where(LevelModel.required_points <= int(u_data["points"])))
        return {"level": level}


    @classmethod
    async def get_all_levels(cls, session: AsyncSession) -> dict[str, Any]:
        result = await session.execute((
            select(BaseUserModel, UserModel, LevelModel)
            .join(UserModel, BaseUserModel.id_bu == UserModel.base_user)  # Замените на ваши реальные имена полей
            .outerjoin(LevelModel.id_l, UserModel.points <= LevelModel.required_points)  # Соединяем по очкам
        ))
        print(result.fetchall())
        return {}
