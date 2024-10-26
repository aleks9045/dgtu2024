from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field



class GoalsCreateSchema(BaseModel):
    name: str
    desc: Optional[str]
    status: str


class ChallengePatchSchema(BaseModel):
    id_ch: int
    name: Optional[str] = Field(default=None)
    desc: Optional[str] = Field(default=None)
    start: Optional[datetime] = Field(default=None)
    end: Optional[datetime] = Field(default=None)
    accepted: Optional[bool] = Field(default=False)
    type: Optional[str] = Field(default=None)
    creator: Optional[str] = Field(default=None)
    title: Optional[str] = Field(title="Achievement", default=None)
    points: Optional[int] = Field(title="Achievement", default=None)