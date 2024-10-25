import httpx
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from starlette.responses import Response

router = APIRouter(
    prefix="/interests",
    tags=["Interests"]
)


async def verify_token(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/auth/token_check",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")


@router.get('/', summary="Get information about user")
async def get_interests(token: str = Depends(verify_token)) -> Response:

    return Response(status_code=200)

# @router.patch('/user', summary="Change user's information")
# async def patch_user(schema: UserPatchSchema,
#                      payload: dict = Depends(existing_user),
#                      session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
#     schema = schema.model_dump()
#     new_data = await UserUpdateQuery.merge_new_n_old(schema, payload, session)
#     await UserUpdateQuery.update_user(new_data, payload, session)
#     return Response(status_code=200)
#
#
# @router.delete('/user', summary="Delete user")
# async def delete_user(payload: dict = Depends(existing_user),
#                       session: AsyncSession = Depends(db_session.get_async_session)) -> Response:
#     await UserDeleteQuery.delete_photo(payload, session)
#     await UserDeleteQuery.delete_user(payload, session)
#     return Response(status_code=200)
