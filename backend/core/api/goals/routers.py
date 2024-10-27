from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from api.goals.schemas import GoalsCreateSchema, GoalsPatchSchema, GoalsIdSchema
from api.goals.utils.goalsquerys import GoalsInsertQuery, GoalsUpdateQuery
from database import db_session
from models import BaseUserModel, UserModel, GoalsModel
from querys import SelectQuery, DeleteQuery
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
    await GoalsInsertQuery.insert(GoalsModel, schema, payload, session)
    return Response(status_code=201)


@router.patch('/', summary="Patch goals")
async def create_goals(schema: GoalsPatchSchema,
                       session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    new_data = await GoalsUpdateQuery.merge_new_n_old(schema, session)
    await GoalsUpdateQuery.update_goals(new_data, session)
    return Response(status_code=200)


@router.delete('/', summary="Delete goal")
async def delete_goal(id_g: int,
                      payload: dict = Depends(verify_token),
                      session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    await DeleteQuery.delete(GoalsModel, GoalsModel.id_g == id_g, session)
    return Response(status_code=200)
