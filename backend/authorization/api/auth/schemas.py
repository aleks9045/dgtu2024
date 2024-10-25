from typing import Optional

from fastapi import UploadFile, File
from pydantic import BaseModel, EmailStr, Field


class UserCreateSchema(BaseModel):
    name: str = Field(title="user's name", max_length=32)
    surname: str = Field(title="user's surname", max_length=32)
    email: EmailStr = Field(title="user's email", max_length=64)
    password: str = Field(title="user's password", max_length=64)

    is_user: bool = Field(default=True)
    is_admin: bool = Field(default=False)


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(title="user's email")
    password: str = Field(title="user's password")


class UserPatchSchema(BaseModel):
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    father_name: Optional[str] = Field(default=None)
    about: Optional[str] = Field(default=None)
    is_user: bool = Field(default=True)


class ForgotPassword(BaseModel):
    email: str = Field(title="user's email")


class ChangePassword(BaseModel):
    password: str = Field(title="user's password")
