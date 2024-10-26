from typing import List

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from api.challenges.schemas import ChallengeCreateSchema, ChallengePatchSchema, ChallengesByEmailsSchema, \
    ChallengesAddUserSchema
from api.challenges.utils.challengesquerys import ChallengesUpdateQuery, ChallengesInsertQuery
from database import db_session
from models import BaseUserModel, UserModel, ChallengesModel, UserChallModel, GlobalAchievementsModel
from querys import SelectQuery
from veryfication import verify_token

router = APIRouter(
    prefix="/challenges",
    tags=["Challenges"]
)


@router.get('/', summary="Get challenges")
async def get_challenges(payload: dict = Depends(verify_token),
                         session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    bu_data = await SelectQuery.select(BaseUserModel.id_bu, BaseUserModel.uu_id == payload["sub"], session)
    return JSONResponse(status_code=200, content=await SelectQuery.join_three(session,
                                                                              ChallengesModel, UserChallModel,
                                                                              UserModel,
                                                                              UserModel.base_user == int(
                                                                                  bu_data["id_bu"]),

                                                                              ChallengesModel.id_ch,
                                                                              UserChallModel.id_ch,

                                                                              UserChallModel.id_u,
                                                                              UserModel.id_u,

                                                                              columns1=ChallengesModel.public_columns,
                                                                              columns3=UserModel.public_columns
                                                                              ))


@router.get('/all', summary="Get all challenges")
async def get_all_challenges(session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    return JSONResponse(status_code=200,
                        content=await SelectQuery.join_two(ChallengesModel, GlobalAchievementsModel, 1 == 1,
                                                           ChallengesModel.id_ch, GlobalAchievementsModel.id_gach,
                                                           session))


@router.post('/', summary="Post challenges")
async def create_challenges(schema: ChallengeCreateSchema,
                            payload: dict = Depends(verify_token),
                            session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    await ChallengesInsertQuery.insert(ChallengesModel, schema, session)
    await ChallengesInsertQuery.insert(GlobalAchievementsModel, schema, session)
    return Response(status_code=201)


@router.patch('/', summary="Patch challenges")
async def patch_challenges(schema: ChallengePatchSchema,
                           payload: dict = Depends(verify_token),
                           session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    new_data = await ChallengesUpdateQuery.merge_new_n_old(schema, session)
    await ChallengesUpdateQuery.update_challenges(new_data, session)
    return Response(status_code=200)

@router.post('/add_user', summary="Add user to challenge")
async def add_user(schema: ChallengesAddUserSchema,
                           payload: dict = Depends(verify_token),
                           session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    await ChallengesInsertQuery.insert(UserChallModel, schema, payload, session)
    return Response(status_code=200)


@router.post('/by_emails', summary="Get challenges by emails")
async def get_challenges_by_emails(schema: List[ChallengesByEmailsSchema],
                            session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    for s in schema:
        print(s.email)
    return Response(status_code=200)