from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field



class ChallengeCreateSchema(BaseModel):
    id_ch: int
    name: str
    desc: str
    rules: str
    status: str
    points: int
    created_at: datetime
    start: datetime
    end: datetime
    photo: Optional[str] = None
    file: Optional[str] = None
    accepted: bool
    type: str



class InterestPatchChema(BaseModel):
    sport: Optional[bool] = Field(default=None)
    cooking: Optional[bool] = Field(default=None)
    art: Optional[bool] = Field(default=None)
    tech: Optional[bool] = Field(default=None)
    communication: Optional[bool] = Field(default=None)
    literature: Optional[bool] = Field(default=None)
    animals: Optional[bool] = Field(default=None)
    games: Optional[bool] = Field(default=None)
    music: Optional[bool] = Field(default=None)
    films: Optional[bool] = Field(default=None)
