from typing import Union, Annotated, Optional

import aiofiles

from fastapi import UploadFile, Depends, HTTPException, File
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRouter
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.schemas import UserLoginSchema, UserPatchSchema, UserCreateSchema
from api.auth.utils.jwt_utils import password, token
from api.auth.utils.router_utils import Checker, SchemaUtils, Files
from api.auth.utils.userquerys import UserSelectQuery, UserInsertQuery, UserUpdateQuery, UserDeleteQuery
from api.querys import SelectQuery
from config import MEDIA_FOLDER
from database import db_session
from models import BaseUserModel, UserModel

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post('/register', summary="Create new user",
             description=f"data field: \n\n```\n\n {SchemaUtils.generate_example(UserCreateSchema)} \n\n```")
async def create_user(schema: UserCreateSchema = Depends(Checker(UserCreateSchema)),
                      photo: UploadFile = File(None),
                      session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    schema = schema.model_dump()
    if not await SelectQuery.exists(BaseUserModel, BaseUserModel.email == schema["email"], session):
        raise HTTPException(status_code=400, detail="Пользователь уже существует.")

    if photo is not None:
        file_path = f'{MEDIA_FOLDER}/user_photos/{photo.filename}'
        await Files.load(file_path, photo)
        schema["photo"] = file_path
    else:
        file_path = f'{MEDIA_FOLDER}/user_photos/default.png'
        schema["photo"] = file_path

    if schema["is_user"]:
        await UserInsertQuery.insert(UserModel, schema, session)
    else:
        raise HTTPException(status_code=400, detail="Не указана роль пользователя.")
    return Response(status_code=201)


@router.post('/login', summary="Create access and refresh tokens")
async def create_new_tokens(schema: UserLoginSchema,
                            session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    schema = schema.model_dump()
    result = await session.execute(
        select(BaseUserModel.uu_id, BaseUserModel.password).where(BaseUserModel.email == schema["email"]))
    result = result.fetchone()
    if not result:
        raise HTTPException(status_code=400, detail="Неверно введена почта или пароль.")
    if not password.verify(schema["password"], result[1]):
        raise HTTPException(status_code=400, detail="Неверно введена почта или пароль.")
    return JSONResponse(status_code=201, content={
        "access": token.create(result[0], type_="access"),
        "refresh": token.create(result[1], type_="refresh")
    })


@router.get('/refresh', summary="Update access and refresh tokens")
async def get_new_tokens(payload: dict = Depends(token.check),
                         session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    if await SelectQuery.exists(BaseUserModel, BaseUserModel.uu_id == payload["sub"], session):
        raise HTTPException(status_code=404)
    return JSONResponse(status_code=200, content={
        "access": token.create(payload["sub"], type_="access"),
        "refresh": token.create(payload["sub"], type_="refresh")
    })

@router.get('/logout', summary="Logout", dependencies=[Depends(token.check)])
async def logout() -> Response:
    return Response(status_code=200)

@router.get('/user', summary="Get information about user")
async def get_user(payload: dict = Depends(token.check),
                   session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    if await SelectQuery.exists(BaseUserModel, BaseUserModel.uu_id == payload["sub"], session):
        raise HTTPException(status_code=404)
    return JSONResponse(status_code=200, content=await UserSelectQuery.get_user(payload, session))


@router.patch('/user', summary="Change user's information")
async def patch_user(schema: UserPatchSchema,
                     payload: dict = Depends(token.check),
                     session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    if await SelectQuery.exists(BaseUserModel, BaseUserModel.uu_id == payload["sub"], session):
        raise HTTPException(status_code=404)
    schema = schema.model_dump()

    new_data = await UserUpdateQuery.merge_new_n_old(schema, payload, session)
    await UserUpdateQuery.update_user(new_data, payload, session)
    return Response(status_code=200)


@router.delete('/user', summary="Delete user")
async def delete_user(payload: dict = Depends(token.check),
                      session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    if await SelectQuery.exists(BaseUserModel, BaseUserModel.uu_id == payload["sub"], session):
        raise HTTPException(status_code=404)

    await UserDeleteQuery.delete_photo(payload, session)
    await UserDeleteQuery.delete_user(payload, session)

    return Response(status_code=200)


@router.patch('/photo', summary="Patch user's photo")
async def delete_photo(payload: dict = Depends(token.check),
                       photo: UploadFile = File(...),
                       session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    if await SelectQuery.exists(BaseUserModel, BaseUserModel.uu_id == payload["sub"], session):
        raise HTTPException(status_code=404)

    file_path = f'{MEDIA_FOLDER}/user_photos/{photo.filename}'
    await UserDeleteQuery.delete_photo(payload, session)
    await Files.load(file_path, photo)

    await session.execute(update(BaseUserModel).where(BaseUserModel.uu_id == payload["sub"]).values(
        photo=f'{MEDIA_FOLDER}/user_photos/{file_path}'))

    return Response(status_code=200)


@router.delete('/photo', summary="Delete user's photo")
async def delete_photo(payload: dict = Depends(token.check),
                       session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
    if await SelectQuery.exists(BaseUserModel, BaseUserModel.uu_id == payload["sub"], session):
        raise HTTPException(status_code=404)
    await UserDeleteQuery.delete_photo(payload, session)

    await session.execute(update(BaseUserModel).where(BaseUserModel.uu_id == payload["sub"]).values(
        photo=f'{MEDIA_FOLDER}/user_photos/default.png'))

    return Response(status_code=200)


@router.get('/all', summary="Get all users")
async def all_user(session: AsyncSession = Depends(db_session.get_async_session)) -> JSONResponse:
    return JSONResponse(status_code=200, content=await UserSelectQuery.get_all_users(session))
