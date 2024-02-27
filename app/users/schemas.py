from typing import List, Optional

from pydantic import BaseModel

# from schedule.schemas import GroupSchema, ProgramSchema
from ..schedule.schemas import GroupSchema
from ..schemas import ProgramSchema, UserSchema


class UserCreateSchema(BaseModel):
    id: int
    telegram_id: int
    name: str
    last_name: str


class UserProgramCreateSchema(UserCreateSchema):
    program_id: int


class UserGroups(UserSchema):
    groups: List[GroupSchema]
