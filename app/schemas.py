from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ProgramName(str, Enum):
    pmi_1 = "pmi_1"
    pmi_2 = "pmi_2"
    pmi_3 = "pmi_3"
    padii_1 = "padii_1"
    padii_2 = "padii_2"


class ProgramBaseSchema(BaseModel):
    name: ProgramName


class ProgramSchema(ProgramBaseSchema):
    id: int


class UserBaseSchema(BaseModel):
    telegram_id: int
    name: str
    last_name: str

    class Config:
        from_attributes = True


class UserGetSchema(UserBaseSchema):
    id: int


class UserSchema(UserBaseSchema):
    id: int
    program: Optional[ProgramSchema]
