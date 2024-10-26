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

from api.interests.schemas import InterestCreateChema
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


@router.get('/', summary="")
async def get_interests(payload: str = Depends(verify_token),
                        session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    return JSONResponse(status_code=200, content=await SelectQuery.join_three(BaseUserModel, UserModel, InterestsModel,
                                                                              BaseUserModel.uu_id == payload["sub"],
                                                                              BaseUserModel.id_bu,
                                                                              UserModel.base_user,
                                                                              InterestsModel.id_i, session))


@router.post('/', summary="")
async def create_interests(schema: InterestCreateChema,
                           payload: dict = Depends(verify_token),
                           session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    bu_data = await SelectQuery.select(BaseUserModel.id_bu, BaseUserModel.uu_id == payload["sub"], session)
    u_data = await SelectQuery.select(UserModel.id_u, UserModel.base_user == int(bu_data["id_bu"]), session)
    schema["id_u"] = int(u_data["id_u"])
    await session.execute(insert(InterestsModel), await BaseQuery.make_one_dict_from_schema(InterestsModel, schema))
    return Response(status_code=201)

    # @router.delete('/user', summary="Delete user")
    # async def delete_user(payload: dict = Depends(existing_user),
    #                       session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    #     await UserDeleteQuery.delete_photo(payload, session)
    #     await UserDeleteQuery.delete_user(payload, session)
    #     return Response(status_code=200)
