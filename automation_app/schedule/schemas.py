from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from users.schemas import UserSchema


class ProgramName(Enum):
    pmi_1 = 'pmi_1'
    pmi_2 = 'pmi_2'
    pmi_3 = 'pmi_3'
    padii_1 = 'padii_1'
    padii_2 = 'padii_2'


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


class ProgramSchema(BaseModel):
    id: int
    name: ProgramName


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
    classroom: str
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
