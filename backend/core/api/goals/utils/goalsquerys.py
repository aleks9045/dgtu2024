from models import ChallengesModel, GlobalAchievementsModel, GoalsModel
from typing import Any, Dict

from sqlalchemy import update, bindparam, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_session
from models import BaseUserModel, UserModel, UserChallModel
from models import ChallengesModel
from querys import SelectQuery, BaseQuery

Base = db_session.base


class GoalsSelectQuery(SelectQuery):
    @classmethod
    async def get_id_u(cls, payload: dict, session: AsyncSession) -> int:
        bu_data = await SelectQuery.select(BaseUserModel.id_bu, BaseUserModel.uu_id == payload["sub"], session)
        u_data = await SelectQuery.select(UserModel.id_u, UserModel.base_user == int(bu_data["id_bu"]), session)
        return int(u_data["id_u"])


class GoalsInsertQuery(BaseQuery):
    @classmethod
    async def insert(cls, model: Base, schema: dict[str, Any], payload: dict, session: AsyncSession):
        schema["id_u"] = await GoalsSelectQuery.get_id_u(payload, session)
        await session.execute(insert(model), await BaseQuery.make_one_dict_from_schema(model, schema))


class GoalsUpdateQuery(BaseQuery):
    @classmethod
    async def merge_new_n_old(cls, schema: dict[str, Any], session: AsyncSession) -> Dict[str, str]:
        old_data = await session.execute(
            select(*GoalsModel.public_columns).where(GoalsModel.id_g == schema["id_g"]))
        col_names = tuple([*old_data._metadata.keys])
        data = old_data.fetchone()

        old_data = await cls.make_dict(data, col_names)
        for key, value in schema.items():
            if schema[key] is None:
                try:
                    if old_data[key] == 'None':
                        schema[key] = None
                    else:
                        schema[key] = old_data[key]
                except KeyError:
                    continue
        return schema

    @classmethod
    async def update_goals(cls, new_data: dict, session: AsyncSession):
        await session.execute(
            update(GoalsModel).where(
                GoalsModel.id_g == new_data["id_g"]).values(
                name=bindparam("name"),
                desc=bindparam("desc"),
                status=bindparam("status")
            ),
            new_data)
