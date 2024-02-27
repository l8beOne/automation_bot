from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from ..schemas import ProgramSchema, UserSchema
# from ..users.schemas import UserSchema





# class GroupName(Enum):
#     maths_analysis = 'maths_analysis'
#     algebra = 'algebra'
#     discrete_maths = 'discrete_maths'
#     algorithms = 'algorithms'
#     java = 'java'
#     english = 'english'
#     prob_theory = 'prob_theory'
#     ml = 'ml'
#     c_plus = 'c_plus'


class SubjectType(Enum):
    lecture = 'lecture'
    practice = 'practice'





class GroupSchema(BaseModel):
    id: int
    name: str
    number: int = Field(ge=1, le=3)

    class Config:
        orm_mode = True


class GroupUsers(GroupSchema):
    users: List[UserSchema]


class SubjectSchema(BaseModel):
    id: int
    name: str
    type: SubjectType
    teacher: str
    zoom_link: Optional[str]
    classroom: Optional[str]
    time: datetime
    group: GroupSchema

    class Config:
        orm_mode = True


class ScheduleSchema(BaseModel):
    id: int
    # program: ProgramSchema
    date: datetime

    class Config:
        orm_mode = True


class ScheduleProgram(ScheduleSchema):
    program: ProgramSchema


class ScheduleSubjectes(ScheduleSchema):
    subjects: List[SubjectSchema]


class ProgramSchedule(ProgramSchema):
    schedules: List[ScheduleSubjectes]