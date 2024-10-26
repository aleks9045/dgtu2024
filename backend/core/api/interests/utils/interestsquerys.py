from typing import Any, Dict

from sqlalchemy import insert, update, bindparam
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_session
from models import BaseUserModel, UserModel, InterestsModel
from querys import SelectQuery, BaseQuery

Base = db_session.base


class InterestsSelectQuery(SelectQuery):
    @classmethod
    async def get_id_u(cls, payload: dict, session: AsyncSession) -> int:
        bu_data = await SelectQuery.select(BaseUserModel.id_bu, BaseUserModel.uu_id == payload["sub"], session)
        u_data = await SelectQuery.select(UserModel.id_u, UserModel.base_user == int(bu_data["id_bu"]), session)
        return int(u_data["id_u"])


    @classmethod
    async def get_all_users(cls, session: AsyncSession) -> Dict[str, Any]:
        data = await cls.join_two(BaseUserModel, UserModel, 1 == 1,
                                  BaseUserModel.id_bu, UserModel.base_user,
                                  session,
                                  columns1=BaseUserModel.public_columns,
                                  columns2=UserModel.public_columns)
        return data


class InterestsInsertQuery(BaseQuery):
    @classmethod
    async def insert(cls, model: Base, schema: dict[str, Any], payload: dict, session: AsyncSession):
        schema["id_u"] = await InterestsSelectQuery.get_id_u(payload, session)
        await session.execute(insert(model), await BaseQuery.make_one_dict_from_schema(model, schema))


class InterestsUpdateQuery(BaseQuery):
    @classmethod
    async def merge_new_n_old(cls, schema: dict[str, Any], payload: dict, session: AsyncSession) -> Dict[str, str]:
        old_data = await SelectQuery.join_three(session,
                                                BaseUserModel, UserModel, InterestsModel,
                                                BaseUserModel.uu_id == payload["sub"],

                                                BaseUserModel.id_bu,
                                                UserModel.base_user,

                                                UserModel.id_u,
                                                InterestsModel.id_u,

                                                BaseUserModel.public_columns,
                                                UserModel.public_columns,
                                                InterestsModel.__table__.columns)
        old_data = old_data[0]
        for key, value in schema.items():
            if schema[key] is None:
                try:
                    if old_data[key] == 'None':
                        schema[key] = None
                    else:
                        schema[key] = old_data[key]
                except KeyError:
                    continue
        schema = {key: bool(value) if isinstance(value, bool) else value.lower() == 'true' for key, value in schema.items()}
        return schema

    @classmethod
    async def update_interests(cls, new_data: dict, payload: dict, session: AsyncSession):
        await session.execute(
            update(InterestsModel).where(InterestsModel.id_u == await InterestsSelectQuery.get_id_u(payload, session)).values(
                sport=bindparam("sport"),
                cooking=bindparam("cooking"),
                art=bindparam("art"),
                tech=bindparam("tech"),
                communication=bindparam("communication"),
                literature=bindparam("literature"),
                animals=bindparam("animals"),
                games=bindparam("games"),
                music=bindparam("music"),
                films=bindparam("films")
            ),
            new_data)
