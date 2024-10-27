from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field



class GoalsCreateSchema(BaseModel):
    name: str
    desc: Optional[str]
    start: Optional[datetime]
    end: Optional[datetime]
    status: str
    steps: int = Field(default=None)
    sleep_millis: int = Field(default=None)


class GoalsPatchSchema(BaseModel):
    id_g: int
    name: Optional[str] = Field(default=None)
    desc: Optional[str] = Field(default=None)
    start: Optional[datetime] = Field(default=None)
    end: Optional[datetime] = Field(default=None)
    status: Optional[str] = Field(default=None)
    steps: int = Field(default=None)
    sleep_millis: int = Field(default=None)

class GoalsByEmailsSchema(BaseModel):
    email: str

class GoalsOrChallengesPatchSchema(BaseModel):
    id: int
    status: Optional[str] = Field(default=None)
    challenges: bool
    goals: bool
