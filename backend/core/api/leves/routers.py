from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from api.leves.utils.levelsquerys import LevelsSelectQuery
from database import db_session
from veryfication import verify_token

router = APIRouter(
    prefix="/levels",
    tags=["Levels"]
)


@router.get('/', summary="Get level")
async def get_level(payload: dict = Depends(verify_token),
                    session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    return JSONResponse(status_code=200, content=await LevelsSelectQuery.get_level(payload, session))



@router.get('/all', summary="Get all levels")
async def get_all_levels(payload: dict = Depends(verify_token),
                    session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    await LevelsSelectQuery.get_all_levels(session)
    return JSONResponse(status_code=200, content={})
