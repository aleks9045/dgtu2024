from typing import List

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from api.statuses.schemas import ChallengesByEmailsSchema, GoalsStatusPatchSchema
from api.statuses.schemas import GoalsByEmailsSchema
from database import db_session
from models import BaseUserModel, UserModel, GoalsModel, ChallengesModel, UserChallModel
from querys import SelectQuery

router = APIRouter(
    prefix="/statuses",
    tags=["Statuses"]
)


@router.post('/challenges_by_emails', summary="Get challenges by emails")
async def get_challenges_by_emails(schema: List[ChallengesByEmailsSchema],
                                   session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    res_dct = {}
    for s in schema:
        res_dct[s.email] = await SelectQuery.join_four(session, ChallengesModel, UserChallModel,
                                                       UserModel, BaseUserModel,
                                                       BaseUserModel.email == s.email,

                                                       UserChallModel.id_ch,
                                                       ChallengesModel.id_ch,

                                                       UserModel.id_u,
                                                       UserChallModel.id_u,

                                                       BaseUserModel.id_bu,
                                                       UserModel.base_user,

                                                       columns1=ChallengesModel.public_columns
                                                       )

    return JSONResponse(status_code=200, content=res_dct)


@router.post('/goals_by_emails', summary="Get goals by emails")
async def get_goals_by_emails(schema: List[GoalsByEmailsSchema],
                              session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    res_dct = {}
    for s in schema:
        res_dct[s.email] = await SelectQuery.join_three(session, GoalsModel, UserModel, BaseUserModel,
                                                        BaseUserModel.email == s.email,

                                                        GoalsModel.id_u,
                                                        UserModel.id_u,

                                                        UserModel.base_user,
                                                        BaseUserModel.id_bu,

                                                        columns1=GoalsModel.public_columns
                                                        )

    return JSONResponse(status_code=200, content=res_dct)


@router.patch('/', summary="Patch goals status")
async def goals_status(schema: GoalsStatusPatchSchema,
                       session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    await session.execute(
        update(GoalsModel).where(GoalsModel.id_g == schema["id"]).values(status=schema["status"]))

    return Response(status_code=200)
