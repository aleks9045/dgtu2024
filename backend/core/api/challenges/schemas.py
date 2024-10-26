from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field



class ChallengeCreateSchema(BaseModel):
    name: str
    desc: Optional[str]
    start: Optional[datetime]
    end: Optional[datetime]
    photo: Optional[str]
    file: Optional[str]
    accepted: bool = Field(default=False)
    type: Optional[str]
    creator: str
    title: str = Field(title="Achievement")
    points: int = Field(title="Achievement")


class ChallengePatchChema(BaseModel):
    id_ch: int
    name: str = Field(default=None)
    desc: Optional[str] = Field(default=None)
    points: int = Field(default=None)
    start: Optional[datetime] = Field(default=None)
    end: Optional[datetime] = Field(default=None)
    photo: Optional[str] = Field(default=None)
    file: Optional[str] = Field(default=None)
    accepted: bool = Field(default=False)
    type: Optional[str] = Field(default=None)
    creator: Optional[str] = Field(default=None)