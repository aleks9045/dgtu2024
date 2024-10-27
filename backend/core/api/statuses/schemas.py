from typing import Optional

from pydantic import BaseModel, Field


class ChallengesByEmailsSchema(BaseModel):
    email: str


class GoalsByEmailsSchema(BaseModel):
    email: str


class GoalsStatusPatchSchema(BaseModel):
    id: int
    status: Optional[str] = Field(default=None)
