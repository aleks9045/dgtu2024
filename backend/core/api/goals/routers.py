from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from api.apiquerys import ApiInsertQuery
from api.interests.schemas import InterestCreateChema, InterestPatchChema
from api.interests.utils.interestsquerys import InterestsUpdateQuery
from database import db_session
from models import BaseUserModel, UserModel, InterestsModel
from querys import SelectQuery
from veryfication import verify_token

router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
)


@router.get('/', summary="Get goals")
async def get_goals(payload: str = Depends(verify_token),
                        session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    return JSONResponse(status_code=200, content=await SelectQuery.join_three(session,
                                                                              BaseUserModel, UserModel, InterestsModel,
                                                                              BaseUserModel.uu_id == payload["sub"],

                                                                              BaseUserModel.id_bu,
                                                                              UserModel.base_user,

                                                                              UserModel.id_u,
                                                                              InterestsModel.id_u,

                                                                              InterestsModel.public_columns))


@router.post('/', summary="Post interests")
async def create_interests(schema: InterestCreateChema,
                           payload: dict = Depends(verify_token),
                           session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    await ApiInsertQuery.insert(InterestsModel, schema, payload, session)
    return Response(status_code=201)


@router.patch('/', summary="Patch interests")
async def create_interests(schema: InterestPatchChema,
                           payload: dict = Depends(verify_token),
                           session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    new_data = await InterestsUpdateQuery.merge_new_n_old(schema, payload, session)
    await InterestsUpdateQuery.update_interests(new_data, payload, session)
    return Response(status_code=200)
