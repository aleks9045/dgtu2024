from typing import Annotated

import httpx
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

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
