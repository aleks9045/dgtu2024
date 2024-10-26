from database import db_session
from models import ChallengesModel
from typing import Any, Dict

from sqlalchemy import update, bindparam
from sqlalchemy.ext.asyncio import AsyncSession

from api.apiquerys import ApiSelectQuery
from database import db_session
from models import BaseUserModel, UserModel, InterestsModel, UserChallModel
from querys import SelectQuery, BaseQuery

Base = db_session.base


class CallengesUpdateQuery(BaseQuery):

    @classmethod
    async def merge_new_n_old(cls, schema: dict[str, Any], payload: dict, session: AsyncSession) -> Dict[str, str]:
        u_data = await ApiSelectQuery.get_id_u(payload, session)
        old_data = await SelectQuery.join_three(session,
                                                UserModel, UserChallModel, ChallengesModel,
                                                UserModel.id_u == u_data["id_u"],

                                                UserModel.id_u,
                                                UserChallModel.id_u,

                                                UserChallModel.id_ch,
                                                ChallengesModel.id_ch,

                                                columns3=ChallengesModel.public_columns)
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
        return schema

    @classmethod
    async def update_challenges(cls, new_data: dict, payload: dict, session: AsyncSession):

        await session.execute(
            update(ChallengesModel).where(
                ChallengesModel.id_ch == await ApiSelectQuery.get_id_ch(payload, session)).values(
                name=bindparam("name"),
                desc=bindparam("desc"),
                rules=bindparam("rules"),
                status=bindparam("status"),
                points=bindparam("points"),
                created_at=bindparam("created_at"),
                start=bindparam("start"),
                end=bindparam("end"),
                photo=bindparam("photo"),
                file=bindparam("file"),
                accepted=bindparam("accepted"),
                type=bindparam("type"),
                creator=bindparam("creator")
            ),
            new_data)
