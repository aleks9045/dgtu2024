from models import ChallengesModel, GlobalAchievementsModel
from typing import Any, Dict

from sqlalchemy import update, bindparam, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_session
from models import BaseUserModel, UserModel, UserChallModel
from models import ChallengesModel
from querys import SelectQuery, BaseQuery

Base = db_session.base


class ChallengesInsertQuery(BaseQuery):
    @classmethod
    async def insert(cls, model: Base, schema: dict[str, Any], payload: dict, session: AsyncSession):
        await session.execute(insert(model), await BaseQuery.make_one_dict_from_schema(model, schema))


class ChallengesSelectQuery(SelectQuery):

    @classmethod
    async def get_id_ch(cls, payload: dict, session: AsyncSession) -> int:
        bu_data = await SelectQuery.select(BaseUserModel.id_bu, BaseUserModel.uu_id == payload["sub"], session)
        u_data = await SelectQuery.select(UserModel.id_u, UserModel.base_user == int(bu_data["id_bu"]), session)
        ch_data = await SelectQuery.select(UserChallModel.id_ch, UserChallModel.id_u == int(u_data["id_u"]), session)
        return int(ch_data["id_ch"])


class ChallengesUpdateQuery(BaseQuery):

    @classmethod
    async def merge_new_n_old(cls, schema: dict[str, Any], payload: dict, session: AsyncSession) -> Dict[str, str]:
        old_data = await session.execute(
            select(*ChallengesModel.public_columns, *GlobalAchievementsModel.public_colums).where(ChallengesModel.id_ch == schema["id_ch"]).join(GlobalAchievementsModel, GlobalAchievementsModel.id_gach == ChallengesModel.id_ch))
        col_names = tuple([*old_data._metadata.keys])
        data = old_data.fetchone()

        old_data = await cls.make_dict(data, col_names)
        print(col_names)
        print(old_data)
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
    async def update_challenges(cls, new_data: dict, payload: dict, session: AsyncSession):

        await session.execute(
            update(ChallengesModel).where(
                ChallengesModel.id_ch == new_data["id_ch"]).values(
                name=bindparam("name"),
                desc=bindparam("desc"),
                start=bindparam("start"),
                end=bindparam("end"),
                accepted=bindparam("accepted"),
                type=bindparam("type"),
                creator=bindparam("creator")
            ),
            new_data)
        await session.execute(
            update(GlobalAchievementsModel).where(
                GlobalAchievementsModel.id_gach == new_data["id_ch"]).values(
                title=bindparam("title"),
                points=bindparam("points")
            ),
            new_data)
