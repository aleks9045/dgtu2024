from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from api.interests.schemas import InterestCreateChema, InterestPatchChema
from api.interests.utils.interestsquerys import InterestsInsertQuery, InterestsUpdateQuery
from database import db_session
from models import BaseUserModel, UserModel, InterestsModel, ChallengesModel, UserChallModel
from querys import SelectQuery
from veryfication import verify_token

router = APIRouter(
    prefix="/challenges",
    tags=["Challenges"]
)


@router.get('/', summary="Get challenges")
async def get_challenges(payload: str = Depends(verify_token),
                         session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    bu_data = await SelectQuery.select(BaseUserModel.id_bu, BaseUserModel.uu_id == payload["sub"], session)
    return JSONResponse(status_code=200, content=await SelectQuery.join_three(session,
                                                                              ChallengesModel, UserChallModel,
                                                                              UserModel,
                                                                              UserModel.id_bu == bu_data["id_bu"],

                                                                              ChallengesModel.id_ch,
                                                                              UserChallModel.id_ch,

                                                                              UserChallModel.id_u,
                                                                              UserModel.id_u,

                                                                              columns1=ChallengesModel.public_columns,
                                                                              columns3=UserModel.public_columns
                                                                              ))


@router.post('/', summary="Post challenges")
async def create_challenges(schema: InterestCreateChema,
                           payload: dict = Depends(verify_token),
                           session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    await InterestsInsertQuery.insert(InterestsModel, schema, payload, session)
    return Response(status_code=201)


@router.patch('/', summary="Patch interests")
async def create_interests(schema: InterestPatchChema,
                           payload: dict = Depends(verify_token),
                           session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    new_data = await InterestsUpdateQuery.merge_new_n_old(schema, payload, session)
    await InterestsUpdateQuery.update_interests(new_data, payload, session)
    return Response(status_code=200)
