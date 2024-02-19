from typing import List, Optional

from pydantic import BaseModel

from schedule.schemas import GroupSchema, ProgramSchema


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
