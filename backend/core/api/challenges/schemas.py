from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field



class ChallengeCreateSchema(BaseModel):
    name: str
    desc: Optional[str]
    start: Optional[datetime]
    end: Optional[datetime]
    accepted: bool = Field(default=False)
    interest: str
    creator: str
    type: Optional[str]
    steps: int = Field(default=None)
    sleep_millis: int = Field(default=None)
    title: str = Field(title="Achievement")
    points: int = Field(title="Achievement")


class ChallengePatchSchema(BaseModel):
    id_ch: int
    name: Optional[str] = Field(default=None)
    desc: Optional[str] = Field(default=None)
    start: Optional[datetime] = Field(default=None)
    end: Optional[datetime] = Field(default=None)
    accepted: Optional[bool] = Field(default=False)
    interest: Optional[str] = Field(default=None)
    creator: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    steps: int = Field(default=None)
    sleep_millis: int = Field(default=None)
    title: Optional[str] = Field(title="Achievement", default=None)
    points: Optional[int] = Field(title="Achievement", default=None)


class ChallengesByEmailsSchema(BaseModel):
    email: str

class ChallengesAddUserSchema(BaseModel):
    id_ch: int