from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field



class ChallengeCreateSchema(BaseModel):
    name: str
    desc: Optional[str]
    rules: Optional[str]
    status: Optional[str]
    points: int
    start: Optional[datetime]
    end: Optional[datetime]
    photo: Optional[str]
    file: Optional[str]
    accepted: bool = Field(default=False)
    type: Optional[str]
    creator: str



class ChallengePatchChema(BaseModel):
    name: str = Field(default=None)
    desc: Optional[str] = Field(default=None)
    rules: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    points: int = Field(default=None)
    start: Optional[datetime] = Field(default=None)
    end: Optional[datetime] = Field(default=None)
    photo: Optional[str] = Field(default=None)
    file: Optional[str] = Field(default=None)
    accepted: bool = Field(default=False)
    type: Optional[str] = Field(default=None)
    creator: Optional[str] = Field(default=None)