from sqlalchemy import AssertionPool, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Group, Program, Schedule, Subject


async def get_sepcific_schedule_crud(user_id, day, session: AsyncSession):
    program_sub_query = (
        select(Program).where(Program.users.any_(id=user_id))
    ).subquery()
    program_qwery = await session.execute(
        select(Program).where(Program.users.any_(id=user_id))
    )
    program = program_qwery.all()
    group_qwery = await session.execute(
        select(Group).where(Group.users.any_(id=user_id))
    )
    groups = group_qwery.all()
    subject_qwery = select(Subject).where(
        or_(Subject.group_id.is_(None), Subject.group.in_(groups))
    )
    qwery = (
        select(Schedule).where(Schedule.program.is_(program_sub_query)).join(Subject)
    )
    result = await session.execute(qwery)
    return result
