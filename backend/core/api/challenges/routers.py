from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy import update, bindparam
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from api.challenges.schemas import ChallengeCreateSchema, ChallengePatchSchema, ChallengesIdSchema, \
    AchievementsAddSchema
from api.challenges.utils.challengesquerys import ChallengesUpdateQuery, ChallengesInsertQuery
from database import db_session
from models import BaseUserModel, UserModel, ChallengesModel, UserChallModel, GlobalAchievementsModel, GAchUserModel
from querys import SelectQuery, DeleteQuery
from veryfication import verify_token

router = APIRouter(
    prefix="/challenges",
    tags=["Challenges and achievements"]
)


@router.get('/by_user', summary="Get challenges by user")
async def get_challenges_by_user(payload: dict = Depends(verify_token),
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

                                                                              columns1=ChallengesModel.public_columns
                                                                              ))


@router.post('/users_by_challenges', summary="Get users by challenges")
async def get_challenges_by_user(schema: ChallengesIdSchema,
                                 payload: dict = Depends(verify_token),
                                 session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    schema = schema.model_dump()
    return JSONResponse(status_code=200, content=await SelectQuery.join_four(session,
                                                                             ChallengesModel, UserChallModel,
                                                                             UserModel, BaseUserModel,
                                                                             ChallengesModel.id_ch == schema["id_ch"],

                                                                             UserChallModel.id_ch,
                                                                             ChallengesModel.id_ch,

                                                                             UserModel.id_u,
                                                                             UserChallModel.id_u,

                                                                             BaseUserModel.id_bu,
                                                                             UserModel.base_user,

                                                                             columns3=UserModel.public_columns,
                                                                             columns4=BaseUserModel.public_columns
                                                                             ))


@router.get('/all', summary="Get all challenge")
async def get_all_challenge(session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    return JSONResponse(status_code=200,
                        content=await SelectQuery.join_two(ChallengesModel, GlobalAchievementsModel, 1 == 1,
                                                           ChallengesModel.id_ch, GlobalAchievementsModel.id_gach,
                                                           session))


@router.post('/', summary="Post challenge")
async def create_challenge(schema: ChallengeCreateSchema,
                           payload: dict = Depends(verify_token),
                           session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    await ChallengesInsertQuery.insert(ChallengesModel, schema, session)
    await ChallengesInsertQuery.insert(GlobalAchievementsModel, schema, session)
    return Response(status_code=201)


@router.patch('/', summary="Patch challenge")
async def patch_challenge(schema: ChallengePatchSchema,
                          payload: dict = Depends(verify_token),
                          session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    new_data = await ChallengesUpdateQuery.merge_new_n_old(schema, session)
    await ChallengesUpdateQuery.update_challenges(new_data, session)
    return Response(status_code=200)


@router.delete('/', summary="Delete challenge")
async def delete_challenge(id_ch: int,
                           session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    await DeleteQuery.delete(ChallengesModel, ChallengesModel.id_ch == id_ch, session)
    return Response(status_code=200)


@router.post('/add_user', summary="Add user to challenge")
async def add_user(schema: ChallengesIdSchema,
                   payload: dict = Depends(verify_token),
                   session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    await ChallengesInsertQuery.insert_with_payload(UserChallModel, schema, payload, session)
    return Response(status_code=200)


@router.post('/add_achievement', summary="Add user to achievement")
async def add_achievement(schema: AchievementsAddSchema,
                          session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()

    await ChallengesInsertQuery.insert(GAchUserModel, schema, session)
    points = await SelectQuery.select(GlobalAchievementsModel.points,
                                      GlobalAchievementsModel.id_gach == schema["id_gach"], session)
    old_points = await SelectQuery.select(UserModel.points, UserModel.id_u == schema["id_u"], session)
    points["points"] += old_points["points"]
    await session.execute(update(UserModel).where(UserModel.id_u == schema["id_u"]).values(
        points=bindparam("points")), points)
    return Response(status_code=200)


@router.get('/achievement', summary="get_achievement")
async def add_achievement(payload: dict = Depends(verify_token),
                          session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    bu_data = await SelectQuery.select(BaseUserModel.id_bu, BaseUserModel.uu_id == payload["sub"], session)
    return JSONResponse(status_code=200, content=await SelectQuery.join_three(session,
                                                                              GlobalAchievementsModel, GAchUserModel,
                                                                              UserModel,
                                                                              UserModel.base_user == int(
                                                                                  bu_data["id_bu"]),

                                                                              GlobalAchievementsModel.id_gach,
                                                                              GAchUserModel.id_gach,

                                                                              GAchUserModel.id_u,
                                                                              UserModel.id_u,

                                                                              columns1=GlobalAchievementsModel.public_columns
                                                                              ))
