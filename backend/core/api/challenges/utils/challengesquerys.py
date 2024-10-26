from database import db_session
from models import ChallengesModel
from typing import Any, Dict

from sqlalchemy import update, bindparam, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.apiquerys import ApiSelectQuery
from database import db_session
from models import BaseUserModel, UserModel, InterestsModel, UserChallModel
from querys import SelectQuery, BaseQuery

Base = db_session.base


class ChallengesUpdateQuery(BaseQuery):

    @classmethod
    async def merge_new_n_old(cls, schema: dict[str, Any], payload: dict, session: AsyncSession) -> Dict[str, str]:
        old_data = await session.execute(select(*ChallengesModel.public_columns).where(ChallengesModel.id_ch == schema["id_ch"]))
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
