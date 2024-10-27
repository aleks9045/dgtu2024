from typing import Any, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_session
from models import BaseUserModel, UserModel, LevelModel
from querys import SelectQuery

Base = db_session.base


class LevelsSelectQuery(SelectQuery):
    @classmethod
    async def get_level(cls, payload: dict, session: AsyncSession) -> dict[str, Any]:
        bu_data = await SelectQuery.select(BaseUserModel.id_bu, BaseUserModel.uu_id == payload["sub"], session)
        u_data = await SelectQuery.select(UserModel.points, UserModel.base_user == int(bu_data["id_bu"]), session)
        level = await session.execute(
            func.max(select(LevelModel.id_l).where(LevelModel.required_points <= int(u_data["points"]))))
        return {"level": level.scalar()}

    @classmethod
    async def get_all_levels(cls, session: AsyncSession) -> List[dict[str, Any]]:
        result = await session.execute((
            select(*BaseUserModel.public_columns,
                   *UserModel.public_columns,
                   func.max(LevelModel.id_l).label("level")).select_from(BaseUserModel)
            .join(
                UserModel, BaseUserModel.id_bu == UserModel.base_user)
            .join(
                LevelModel,
                UserModel.points <= LevelModel.required_points)
            .group_by(
                *BaseUserModel.public_columns, *UserModel.public_columns)
        ))
        col_names = tuple([*result._metadata.keys])
        data = tuple(result.all())
        return await cls.make_list_of_dicts(data, col_names)
