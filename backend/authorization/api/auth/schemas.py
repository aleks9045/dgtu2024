from typing import Optional

from fastapi import UploadFile, File
from pydantic import BaseModel, EmailStr, Field


class UserCreateSchema(BaseModel):
    first_name: str = Field(title="user's first_name", max_length=32)
    last_name: str = Field(title="user's last_name", max_length=32)
    father_name: str = Field(title="user's father_name", max_length=32)
    email: EmailStr = Field(title="user's email", max_length=64)
    password: str = Field(title="user's password", max_length=64)

    about: str = Field(title="about user", max_length=255, default=None)
    is_user: bool = Field(default=True)


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(title="user's email")
    password: str = Field(title="user's password")


class UserPatchSchema(BaseModel):
    first_name: Optional[str] = Field(title="user's first_name", default=None)
    last_name: Optional[str] = Field(title="user's last_name", default=None)
    father_name: Optional[str] = Field(title="user's father_name", default=None)
    about: Optional[str] = Field(title="about user", default=None)
    is_user: bool = Field(default=True)


class ChangeEmail(BaseModel):
    email: str = Field(title="user's email")


class ChangePassword(BaseModel):
    password: str = Field(title="user's password")
