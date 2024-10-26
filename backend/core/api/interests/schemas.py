from typing import Optional

from pydantic import BaseModel, Field



class InterestCreateChema(BaseModel):
    sport: bool
    cooking: bool
    art: bool
    tech: bool
    communication: bool
    literature: bool
    animals: bool
    games: bool
    music: bool
    films: bool


class ForgotPassword(BaseModel):
    email: str = Field(title="user's email")


class ChangePassword(BaseModel):
    password: str = Field(title="user's password")
