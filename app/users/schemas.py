from typing import List, Optional

from ..schedule.schemas import GroupSchema
from ..schemas import UserSchema, UserBaseSchema


class UserCreateSchema(UserBaseSchema):
    telegram_id: int
    name: str
    last_name: str


class UserProgramCreateSchema(UserCreateSchema):
    program_id: int

    class Config:
        from_attributes = True


class UserGroups(UserSchema):
    groups: Optional[List[GroupSchema]]

    class Config:
        from_attributes = True
