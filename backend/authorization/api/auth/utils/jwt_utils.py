import datetime
from typing import Union, Any, Annotated

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from passlib.context import CryptContext

from config import SECRET_JWT_ACCESS, SECRET_JWT_REFRESH, JWT_ALGORITHM, TIME_OFFSET

security = HTTPBearer(auto_error=True)


class Password:
    def __init__(self):
        self.password_context = CryptContext(schemes=["bcrypt"])

    def hash(self, user_password: str) -> str:
        return self.password_context.hash(user_password)

    def verify(self, user_password: str, hashed_pass: str) -> bool:
        return self.password_context.verify(user_password, hashed_pass)


class Token:
    def __init__(self,
                 access_time: int = 120,  # 15 minutes
                 refresh_time: int = 60 * 24 * 7 * 2,  # 14 days
                 algorithm: str = JWT_ALGORITHM):
        self.ACCESS_TOKEN_EXPIRE_MINUTES = access_time
        self.REFRESH_TOKEN_EXPIRE_MINUTES = refresh_time
        self.ALGORITHM = algorithm
        self._JWT_ACCESS_SECRET_KEY = SECRET_JWT_ACCESS
        self._JWT_REFRESH_SECRET_KEY = SECRET_JWT_REFRESH

    def create(self, subject: Union[str, Any], type_: str) -> str:
        if type_ == "access":
            expire = self.ACCESS_TOKEN_EXPIRE_MINUTES
            key = self._JWT_ACCESS_SECRET_KEY
        elif type_ == "refresh":
            expire = self.REFRESH_TOKEN_EXPIRE_MINUTES
            key = self._JWT_REFRESH_SECRET_KEY
        else:
            raise ValueError("Неверно указан тип токена")
        expires_delta = datetime.datetime.now(TIME_OFFSET) + datetime.timedelta(
            minutes=expire)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, key, self.ALGORITHM)
        return encoded_jwt

    async def check(self, authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)],
                    type_: str = "access") -> dict:
        try:
            jwt_token = authorization.credentials
            if type_ == "access":
                payload = jwt.decode(jwt_token, self._JWT_ACCESS_SECRET_KEY, algorithms=[self.ALGORITHM])
            elif type_ == "refresh":
                payload = jwt.decode(jwt_token, self._JWT_REFRESH_SECRET_KEY, algorithms=[self.ALGORITHM])
            else:
                raise ValueError("Неверно указан тип токена")
            if datetime.datetime.fromtimestamp(payload["exp"]).timestamp() < \
                    datetime.datetime.now(TIME_OFFSET).timestamp():
                raise HTTPException(status_code=401,
                                    detail="Срок действия токена истёк.")
        except jwt.JWTError:
            raise HTTPException(status_code=403,
                                detail="Не удалось подтвердить учетные данные.")
        return payload


password = Password()
token = Token()
