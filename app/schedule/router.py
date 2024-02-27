from datetime import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import and_, any_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..database import get_async_session
from ..models import Group, GroupUsers, Program, Schedule, Subject, User
from .schemas import ScheduleSubjectes
from .utils import check_date_for_schedule

from .crud import get_sepcific_schedule_crud


router_schedule = APIRouter(prefix="/schedule", tags=["Schedule"])


@router_schedule.post("/")
async def create_schedule(
    # request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    ...


@router_schedule.post("/subjects")
async def update_subjects(*args, **kwargs):
    ...


@router_schedule.get("/{user_id}/{day}/", response_model=ScheduleSubjectes)
async def get_specific_schedule(
    user_id: int, day: str, session: AsyncSession = Depends(get_async_session)
):
    # user_result = await session.execute(select(User).where(User.id == user_id))
    # user = user_result.scalars().one()


    ### пример того что имеет право быть в роутере
    # if user_id in ban_list:
    #     raise HTTPException(400, "ты кто?")



    result = await get_sepcific_schedule_crud(user_id, day, session)
    
    # qwery = select(Schedule).\
    #         filter(check_date_for_schedule(Schedule.date) == True).\
    #         where(user.in_ Schedule.program.users).\
    #         filter(Schedule.program.any(users))
    # join(Schedule.subjects).\
    # filter(Subject.group_id.in_([None, user.groups]) == None or user.in_(Subject.group.users))
    
    return result.all()
