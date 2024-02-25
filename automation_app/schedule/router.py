from datetime import datetime as dt

from fastapi import APIRouter, Depends
from sqlalchemy import select, or_, and_, any_
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from schedule.schemas import ScheduleSubjectes
from models import Schedule, User, Program, Group, GroupUsers, Subject
from utils import check_date_for_schedule


router_schedule = APIRouter(
    prefix='/schedule',
    tags=['Schedule']
)

@router_schedule.post('/')
async def create_schedule(*args, **kwargs):
    return


@router_schedule.post('/subjects')
async def update_subjects(*args, **kwargs):
    return


@router_schedule.get('/{user_id}/{day}/', response_model=ScheduleSubjectes)
async def get_specific_schedule(user_id : int, session: AsyncSession = Depends(get_async_session)):
    # user_result = await session.execute(select(User).where(User.id == user_id))
    # user = user_result.scalars().one()
    program_sub_query = (select(Program).where(Program.users.any_(id=user_id))).subquery()
    program_qwery = await session.execute(select(Program).where(Program.users.any_(id=user_id)))
    program = program_qwery.all()
    group_qwery = await session.execute(select(Group).where(Group.users.any_(id=user_id)))
    groups = group_qwery.all()
    subject_qwery = select(Subject).where(or_(Subject.group_id.is_(None), Subject.group.in_(groups)))
    qwery = select(Schedule).where(Schedule.program.is_(program_sub_query)).join(Subject)



    # qwery = select(Schedule).\
    #         filter(check_date_for_schedule(Schedule.date) == True).\
    #         where(user.in_ Schedule.program.users).\
    #         filter(Schedule.program.any(users))
            # join(Schedule.subjects).\
            # filter(Subject.group_id.in_([None, user.groups]) == None or user.in_(Subject.group.users))
    result = await session.execute(qwery)
    return result.all()
