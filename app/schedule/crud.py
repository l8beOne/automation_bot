from datetime import date
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import Group, Program, Schedule, SheduleSubjects, Subject
from ..schemas import ProgramBaseSchema, ProgramName
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


async def create_schedule_crud(
    new_schedule: ScheduleBaseSchema,
    program_name: ProgramName,
    session: AsyncSession
):
    program_result = await session.execute(
        select(Program.id).where(
            Program.name == program_name
        )
    )
    schedule_program_id = program_result.scalar()
    if not schedule_program_id:
        return {
            "status": "error",
            "status_code": 400,
            "detail": "No program for this schedule"
        }
    schedule_result = await session.execute(
        select(Schedule).where(
            Schedule.date == new_schedule.date and
            Schedule.program_id == schedule_program_id
        )
    )
    session_schedule = schedule_result.scalar()
    if session_schedule:
        return {
            "status": "error",
            "status_code": 400,
            "detail": "Schedule already exists"
        }
    await session.execute(
        insert(Schedule).values(
            **new_schedule.model_dump(),
            program_id = schedule_program_id
        )
    )
    await session.commit()
    result = await session.execute(
        select(Schedule).where(
            Schedule.date == new_schedule.date and
            Schedule.program_id == schedule_program_id
        )
    )
    return result.scalars()


async def create_program_crud(
    new_program: ProgramBaseSchema,
    session: AsyncSession
):
    result = await session.execute(select(Program).where(Program.name == new_program.name))
    session_program = result.scalar()
    if session_program:
        return {
            "status": "error",
            "status_code": 400,
            "detail": "Program already registered"
        }
    else:
        await session.execute(insert(Program).values(**new_program.model_dump()))
        await session.commit()
        result = await session.execute(select(Program).where(Program.name == new_program.name))
        return result.scalars()


async def get_programs_crud(session: AsyncSession):
    qwery = select(Program)
    result = await session.execute(qwery)
    return result.scalars()


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
        return {
            "status": "error",
            "status_code": 400,
            "detail": "Group already registered"
        }
    else:
        stmt = insert(Group).values(**new_group.model_dump())
        await session.execute(stmt)
        await session.commit()
        qwery = select(Group).where(Group.name == new_group.name)
        result = await db.execute(qwery)
        return result.scalars()


async def get_groups_crud(session: AsyncSession):
    qwery = select(Group)
    result = await session.execute(qwery)
    return result.scalars()


async def create_subject_crud(
    new_subjects: List[SubjectBaseSchema],
    schedule_date: date,
    session: AsyncSession
):
    schedule_exists_result = await session.execute(
        select(Schedule.id).where(
            Schedule.date == schedule_date
        )
    )
    schedule_id = schedule_exists_result.scalar()
    if not schedule_id:
        return {
            "status": "error",
            "status_code": 400,
            "detail": "no schedule for this date"
        }
    for new_subject in new_subjects:
        subject_exists_result = await session.execute(
            select(Subject.id).where(
                Subject.classroom == new_subject.classroom and
                Subject.name == new_subject.name and
                Subject.teacher == new_subject.teacher and
                Subject.time == new_subject.time and
                Subject.type == new_subject.type and
                Subject.zoom_link == new_subject.zoom_link
            )
        )
        subject_id = subject_exists_result.scalar()
        if subject_id:
            schedule_subjects = await session.execute(
                select(Schedule.id).where(
                    Schedule.subjects.any(id=subject_id)
                )
            )
            schedule_subjects_result = schedule_subjects.scalars()
            if schedule_id not in schedule_subjects_result:
                await session.execute(
                    insert(SheduleSubjects).values(
                        subject_id=subject_id,
                        schedule_id=schedule_id
                    )
                )
                await session.commit()
        else:
            group_exists_result = await session.execute(
                select(Group.id).where(
                    Group.name == new_subject.name
                )
            )
            group_id = group_exists_result.scalar()
            if group_id:
                await session.execute(
                    insert(Subject).values(
                        **new_subject.model_dump(),
                        group_id = group_id
                    )
                )
                await session.commit()
            else:
                await session.execute(
                    insert(Subject).values(
                        **new_subject.model_dump()
                    )
                )
                await session.commit()
            subject_exists_result = await session.execute(
                select(Subject.id).where(
                    Subject.classroom == new_subject.classroom and
                    Subject.name == new_subject.name and
                    Subject.teacher == new_subject.teacher and
                    Subject.time == new_subject.time and
                    Subject.type == new_subject.type and
                    Subject.zoom_link == new_subject.zoom_link
                )
            )
            subject_id = subject_exists_result.scalar()
            await session.execute(
                insert(SheduleSubjects).values(
                    subject_id=subject_id,
                    schedule_id=schedule_id
                )
            )
            await session.commit()
    return {"status": "success"}


async def get_subjects_crud(session: AsyncSession):
    qwery = select(Subject)
    result = await session.execute(qwery)
    return result
