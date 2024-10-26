from typing import Any, Dict

from sqlalchemy import update, bindparam
from sqlalchemy.ext.asyncio import AsyncSession

from api.apiquerys import ApiSelectQuery
from database import db_session
from models import BaseUserModel, UserModel, InterestsModel, ChallengesModel
from querys import SelectQuery, BaseQuery

Base = db_session.base


class CallengesUpdateQuery(BaseQuery):


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
