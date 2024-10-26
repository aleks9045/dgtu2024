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
