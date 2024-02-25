from typing import List, Optional

from pydantic import BaseModel

from schedule.schemas import GroupSchema, ProgramSchema


class UserCreateSchema(BaseModel):
    id: int
    telegram_id: int
    name: str
    last_name: str


class UserProgramCreateSchema(UserCreateSchema):
    program_id: int


class UserSchema(BaseModel):
    id: int
    telegram_id: int
    name: str
    last_name: str
    program: Optional[ProgramSchema]

    class Config:
        orm_mode = True


class UserGroups(UserSchema):
    groups: List[GroupSchema]
