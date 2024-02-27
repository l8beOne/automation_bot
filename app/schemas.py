from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ProgramName(Enum):
    pmi_1 = "pmi_1"
    pmi_2 = "pmi_2"
    pmi_3 = "pmi_3"
    padii_1 = "padii_1"
    padii_2 = "padii_2"


class ProgramSchema(BaseModel):
    id: int
    name: ProgramName


class UserSchema(BaseModel):
    id: int
    telegram_id: int
    name: str
    last_name: str
    program: Optional[ProgramSchema]

    class Config:
        orm_mode = True
