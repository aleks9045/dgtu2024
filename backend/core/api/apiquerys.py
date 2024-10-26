from typing import Any, Dict

from sqlalchemy import insert, update, bindparam, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_session
from models import BaseUserModel, UserModel, ChallengesModel, UserChallModel
from querys import SelectQuery, BaseQuery

Base = db_session.base


class ApiSelectQuery(SelectQuery):
    @classmethod
    async def get_id_u(cls, payload: dict, session: AsyncSession) -> int:
        bu_data = await SelectQuery.select(BaseUserModel.id_bu, BaseUserModel.uu_id == payload["sub"], session)
        u_data = await SelectQuery.select(UserModel.id_u, UserModel.base_user == int(bu_data["id_bu"]), session)
        return int(u_data["id_u"])

    @classmethod
    async def get_id_ch(cls, payload: dict, session: AsyncSession) -> int:
        bu_data = await SelectQuery.select(BaseUserModel.id_bu, BaseUserModel.uu_id == payload["sub"], session)
        u_data = await SelectQuery.select(UserModel.id_u, UserModel.base_user == int(bu_data["id_bu"]), session)
        ch_data = await SelectQuery.select(UserChallModel.id_ch, UserChallModel.id_u == int(u_data["id_u"]), session)
        return int(ch_data["id_ch"])

class ApiInsertQuery(BaseQuery):
    @classmethod
    async def insert(cls, model: Base, schema: dict[str, Any], payload: dict, session: AsyncSession):
        schema["id_u"] = await ApiSelectQuery.get_id_u(payload, session)
        await session.execute(insert(model), await BaseQuery.make_one_dict_from_schema(model, schema))
