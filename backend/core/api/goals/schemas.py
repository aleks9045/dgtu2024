from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field



class GoalsCreateSchema(BaseModel):
    name: str
    desc: Optional[str]
    start: Optional[datetime]
    end: Optional[datetime]
    status: str


class GoalsPatchSchema(BaseModel):
    id_g: int
    name: Optional[str] = Field(default=None)
    desc: Optional[str] = Field(default=None)
    start: Optional[datetime] = Field(default=None)
    end: Optional[datetime] = Field(default=None)
    status: Optional[str] = Field(default=None)