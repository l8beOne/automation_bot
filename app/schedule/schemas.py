from datetime import datetime, date, time
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from ..schemas import ProgramSchema, UserSchema


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


class SubjectType(str, Enum):
    lecture = 'lecture'
    practice = 'practice'


class GroupBaseSchema(BaseModel):
    name: str
    # number: int = Field(ge=1, le=3)

    class Config:
        from_attributes = True


class GroupSchema(GroupBaseSchema):
    id: int


class GroupUsers(GroupBaseSchema):
    id: int
    users: List[UserSchema]


class SubjectBaseSchema(BaseModel):
    name: str
    type: SubjectType
    teacher: str
    zoom_link: Optional[str] = None
    classroom: Optional[str] = None
    time: time

    class Config:
        from_attributes = True


class SubjectGetSchema(SubjectBaseSchema):
    id: int


class SubjectSchema(SubjectBaseSchema):
    id: int
    group: GroupSchema


class ScheduleBaseSchema(BaseModel):
    date: date

    class Config:
        from_attributes = True


class ScheduleSchema(ScheduleBaseSchema):
    id: int


class ScheduleProgram(ScheduleSchema):
    id: int
    program: ProgramSchema


class ScheduleSubjects(ScheduleSchema):
    subjects: List[SubjectSchema]


# class ProgramSchedule(ProgramSchema): вряд ли будет нужна
#     schedules: List[ScheduleSubjects]
