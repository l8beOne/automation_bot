from fastapi import Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..models import Group, Program, Subject
from ..schemas import ProgramBaseSchema
from .schemas import GroupBaseSchema, ScheduleBaseSchema, SubjectBaseSchema


async def get_sepcific_schedule_crud(
    user_id,
    day,
    session: AsyncSession
):
    ...
    # program_sub_query = (
    #     select(Program).where(Program.users.any_(id=user_id))
    # ).subquery()
    # program_qwery = await session.execute(
    #     select(Program).where(Program.users.any_(id=user_id))
    # )
    # program = program_qwery.all()
    # group_qwery = await session.execute(
    #     select(Group).where(Group.users.any_(id=user_id))
    # )
    # groups = group_qwery.all()
    # subject_qwery = select(Subject).where(
    #     or_(Subject.group_id.is_(None), Subject.group.in_(groups))
    # )
    # qwery = (
    #     select(Schedule).where(Schedule.program.is_(program_sub_query)).join(Subject)
    # )
    # result = await session.execute(qwery)
    # return result


async def create_schedule(
    new_schedule: ScheduleBaseSchema,
    db: AsyncSession = Depends(get_async_session)
):
    ...


async def create_program_crud(
    new_program: ProgramBaseSchema,
    session: AsyncSession,
    db: AsyncSession
):
    qwery = select(Program).where(Program.name == new_program.name)
    result = await db.execute(qwery)
    db_program = result.scalar()
    if db_program:
        raise HTTPException(
            status_code=400,
            detail="Program already registered"
        )
    else:
        stmt = insert(Program).values(**new_program.model_dump())
        await session.execute(stmt)
        await session.commit()
        qwery = select(Program).where(Program.name == new_program.name)
        result = await db.execute(qwery)
        return result


async def get_programs_crud(session: AsyncSession):
    qwery = select(Program)
    result = await session.execute(qwery)
    return result


async def create_group_crud(
    new_group: GroupBaseSchema,
    session: AsyncSession,
    db: AsyncSession
):
    qwery = select(Group).where(Group.name == new_group.name)
    result = await db.execute(qwery)
    db_group = result.scalar()
    print(db_group)
    if db_group:
        raise HTTPException(
            status_code=400,
            detail="Group already registered"
        )
    else:
        stmt = insert(Group).values(**new_group.model_dump())
        await session.execute(stmt)
        await session.commit()
        qwery = select(Group).where(Group.name == new_group.name)
        result = await db.execute(qwery)
        return result


async def get_groups_crud(session: AsyncSession):
    qwery = select(Group)
    result = await session.execute(qwery)
    return result


async def create_subject_crud(
    new_subject: SubjectBaseSchema,
    session: AsyncSession
):
    stmt = insert(Subject).values(**new_subject.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


async def get_subjects_crud(session: AsyncSession):
    qwery = select(Subject)
    result = await session.execute(qwery)
    return result
