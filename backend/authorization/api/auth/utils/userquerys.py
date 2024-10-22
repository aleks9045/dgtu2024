import uuid
from typing import Any, Dict

from sqlalchemy import insert, update, bindparam
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.utils.jwt_utils import password
from api.auth.utils.router_utils import Files
from api.querys import SelectQuery, BaseQuery, DeleteQuery
from config import MEDIA_FOLDER
from database import db_session
from models import BaseUserModel, AdminModel, UserModel

Base = db_session.base


class UserSelectQuery(SelectQuery):
    @classmethod
    async def get_user(cls, payload: dict, session: AsyncSession) -> Dict[str, Any]:
        data = await cls.join_two(BaseUserModel, UserModel,
                                  BaseUserModel.uu_id == payload["sub"],
                                  BaseUserModel.id_bu, UserModel.baseuser,
                                  session,
                                  columns1=BaseUserModel.public_columns,
                                  columns2=UserModel.public_columns)
        return data[0]


    @classmethod
    async def get_admin(cls, payload: dict, session: AsyncSession) -> Dict[str, Any]:
        data = await cls.join_two(BaseUserModel, AdminModel,
                                  BaseUserModel.uu_id == payload["sub"],
                                  BaseUserModel.id_bu, AdminModel.baseuser,
                                  session,
                                  columns1=BaseUserModel.public_columns)
        return data[0]

    @classmethod
    async def get_all_users(cls, session: AsyncSession) -> Dict[str, Any]:
        data = await cls.join_two(BaseUserModel, UserModel, 1 == 1,
                                  BaseUserModel.id_bu, UserModel.baseuser,
                                  session,
                                  columns1=BaseUserModel.public_columns,
                                  columns2=UserModel.public_columns)
        return data


class UserInsertQuery(BaseQuery):
    @classmethod
    async def insert(cls, model: Base, schema: dict[str, Any], session: AsyncSession):
        bu_data = await cls.make_one_dict_from_schema(BaseUserModel, schema)
        bu_data['uu_id'] = str(uuid.uuid1())
        bu_data['password'] = password.hash(schema["password"])

        result = await session.execute(insert(BaseUserModel).returning(BaseUserModel.id_bu), bu_data)
        id_bu = result.scalars().one()
        u_data = await cls.make_one_dict_from_schema(model, schema)
        u_data['baseuser'] = id_bu

        await session.execute(insert(model), u_data)



class UserUpdateQuery(BaseQuery):
    @classmethod
    async def merge_new_n_old(cls, schema: dict[str, Any], payload: dict, session: AsyncSession) -> Dict[str, str]:
        old_data = await UserSelectQuery.get_user(payload, session)
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
    async def update_user(cls, new_data: dict, payload: dict, session: AsyncSession):
        id_bu = await session.execute(
            update(BaseUserModel).where(BaseUserModel.uu_id == payload["sub"]).values(
                first_name=bindparam("first_name"),
                last_name=bindparam("last_name"),
                father_name=bindparam("father_name")).returning(BaseUserModel.id_bu),
            new_data)
        await session.execute(
            update(UserModel).where(UserModel.baseuser == id_bu.fetchone()[0]).values(
                about=bindparam("about")),
            new_data)



class UserDeleteQuery(DeleteQuery):
    @classmethod
    async def delete_user(cls, payload: dict, session: AsyncSession):
        id_bu = await SelectQuery.select(BaseUserModel.id_bu, BaseUserModel.uu_id == payload["sub"], session)
        id_bu = int(id_bu["id_bu"])
        await cls.delete(UserModel, UserModel.baseuser == id_bu, session)
        await cls.delete(BaseUserModel, BaseUserModel.id_bu == id_bu, session)

    @classmethod
    async def delete_photo(cls, payload: dict, session: AsyncSession):
        user_photo = await SelectQuery.select(BaseUserModel.photo, BaseUserModel.uu_id == payload["sub"], session)
        if user_photo["photo"] != f'{MEDIA_FOLDER}/user_photos/default.png':
            await Files.delete(user_photo["photo"])
