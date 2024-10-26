from typing import Annotated

import httpx
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.leves.utils.levelsquerys import LevelsSelectQuery
from database import db_session
from models import BaseUserModel, UserModel, InterestsModel, LevelModel
from querys import SelectQuery

router = APIRouter(
    prefix="/levels",
    tags=["Levels"]
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


@router.get('/', summary="Get level")
async def get_level(payload: dict = Depends(verify_token),
                    session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    return JSONResponse(status_code=200, content=await LevelsSelectQuery.get_points(payload, session))
