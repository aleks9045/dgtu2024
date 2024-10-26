from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from api.goals.schemas import GoalsCreateSchema
from api.goals.utils.goalsquerys import GoalsSelectQuery, GoalsInsertQuery
from api.interests.schemas import InterestCreateSchema, InterestPatchSchema
from api.interests.utils.interestsquerys import InterestsUpdateQuery
from database import db_session
from models import BaseUserModel, UserModel, InterestsModel, GoalsModel
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
                                                                              BaseUserModel, UserModel, GoalsModel,
                                                                              BaseUserModel.uu_id == payload["sub"],

                                                                              BaseUserModel.id_bu,
                                                                              UserModel.base_user,

                                                                              UserModel.id_u,
                                                                              GoalsModel.id_u,

                                                                              columns3=GoalsModel.public_columns))


@router.post('/', summary="Post goals")
async def create_goals(schema: GoalsCreateSchema,
                           payload: dict = Depends(verify_token),
                           session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    await GoalsInsertQuery.insert(InterestsModel, schema, payload, session)
    return Response(status_code=201)


@router.patch('/', summary="Patch goals")
async def create_goals(schema: InterestPatchSchema,
                       payload: dict = Depends(verify_token),
                       session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    new_data = await InterestsUpdateQuery.merge_new_n_old(schema, payload, session)
    await InterestsUpdateQuery.update_interests(new_data, payload, session)
    return Response(status_code=200)
