from typing import Annotated

import httpx
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from api.interests.schemas import InterestCreateChema, InterestPatchChema
from api.interests.utils.interestsquerys import InterestsInsertQuery, InterestsUpdateQuery
from database import db_session
from models import BaseUserModel, UserModel, InterestsModel
from querys import SelectQuery, BaseQuery

router = APIRouter(
    prefix="/interests",
    tags=["Interests"]
)

security = HTTPBearer(auto_error=True)


async def verify_token(token: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://authorization:8000/auth/token_check",
            headers={"Authorization": f"Bearer {token.credentials}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        return response.json()


@router.get('/', summary="Get interests")
async def get_challenges(payload: str = Depends(verify_token),
                        session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    return JSONResponse(status_code=200, content=await SelectQuery.join_three(session,
                                                                              BaseUserModel, UserModel, InterestsModel,
                                                                              BaseUserModel.uu_id == payload["sub"],

                                                                              BaseUserModel.id_bu,
                                                                              UserModel.base_user,

                                                                              UserModel.id_u,
                                                                              InterestsModel.id_u,

                                                                              BaseUserModel.public_columns,
                                                                              UserModel.public_columns,
                                                                              InterestsModel.__table__.columns))


@router.post('/', summary="Post interests")
async def create_interests(schema: InterestCreateChema,
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
