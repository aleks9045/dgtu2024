from typing import Any, Dict

from sqlalchemy import insert, update, bindparam
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_session
from models import BaseUserModel, UserModel, InterestsModel
from querys import SelectQuery, BaseQuery

Base = db_session.base

class LevelsSelectQuery(SelectQuery):
    @classmethod
    async def get_points(cls, payload: dict, session: AsyncSession) -> dict[str, Any]:
        bu_data = await SelectQuery.select(BaseUserModel.id_bu, BaseUserModel.uu_id == payload["sub"], session)
        u_data = await SelectQuery.select(UserModel.points, UserModel.base_user == int(bu_data["id_bu"]), session)
        return u_data