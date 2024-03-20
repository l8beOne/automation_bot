from datetime import date
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy import and_, or_, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import Group, Program, Schedule, SheduleSubjects, Subject, User
from ..schemas import ProgramBaseSchema, ProgramName
from .schemas import GroupBaseSchema, ScheduleBaseSchema, SubjectBaseSchema


async def get_sepcific_schedule_crud(
    user_telegram_id: int,
    day: date,
    session: AsyncSession
):
    user = await session.execute(
        select(User.id, User.program_id).where(User.telegram_id == user_telegram_id)
    )
    user_result = user.first()
    user_id = user_result[0]
    user_program_id = user_result[1]
    if not user_id:
        return {
            "status": "error",
            "status_code": 404,
            "detail": "No user with this telegram_id"
        }
    if not user_program_id:
        return {
            "status": "error",
            "status_code": 404,
            "detail": "User must choose program"
        }

    schedule = await session.execute(
        select(Schedule.id).where(
            Schedule.program_id == user_program_id and
            Schedule.date == day
        )
    )
    user_schedule_id = schedule.scalar()
    if not user_schedule_id:
        return {
            "status": "error",
            "status_code": 404,
            "detail": "No schedule for this date and program"
        }
    
    groups = await session.execute(select(Group.id).where(Group.users.any(id=user_id)))
    user_groups = [group_id for group_id in groups.scalars()] + [None,]
    print(user_groups)

    subjects = await session.execute(
        select(Subject).where(
            and_(Subject.group_id.in_(user_groups),
            Subject.schedules.any(id=user_schedule_id))
        )
    )
    return subjects.scalars()


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
    group = await db.execute(select(Group).where(Group.name == new_group.name))
    db_group = group.scalar()
    if db_group:
        return {
            "status": "error",
            "status_code": 400,
            "detail": "Group already registered"
        }
    else:
        await session.execute(insert(Group).values(**new_group.model_dump()))
        await session.commit()
        result = await db.execute(select(Group).where(Group.name == new_group.name))
        return result.scalars()


async def get_groups_crud(session: AsyncSession):
    qwery = select(Group)
    result = await session.execute(qwery)
    return result.scalars()


async def create_subject_crud(
    new_subjects: List[SubjectBaseSchema],
    schedule_date: date,
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
    schedule_exists_result = await session.execute(
        select(Schedule.id).where(
            and_(
                Schedule.date == schedule_date,
                Schedule.program_id == schedule_program_id
            )
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
                and_(
                    Subject.classroom == new_subject.classroom,
                    Subject.name == new_subject.name,
                    Subject.teacher == new_subject.teacher,
                    Subject.time == new_subject.time,
                    Subject.type == new_subject.type,
                    Subject.zoom_link == new_subject.zoom_link
                )
            )
        )
        subject_id = subject_exists_result.scalar()
        if subject_id:
            print(subject_id)
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
            print(1)
            group_exists_result = await session.execute(
                select(Group.id).where(
                    Group.name == new_subject.name
                )
            )
            group_id = group_exists_result.scalar()
            if group_id:
                print(group_id)
                await session.execute(
                    insert(Subject).values(
                        **new_subject.model_dump(),
                        group_id = group_id
                    )
                )
                await session.commit()
                print(2)
            else:
                await session.execute(
                    insert(Subject).values(
                        **new_subject.model_dump()
                    )
                )
                await session.commit()
                print(3)
            subject_exists_result = await session.execute(
                select(Subject.id).where(
                    and_(
                        Subject.classroom == new_subject.classroom,
                        Subject.name == new_subject.name,
                        Subject.teacher == new_subject.teacher,
                        Subject.time == new_subject.time,
                        Subject.type == new_subject.type,
                        Subject.zoom_link == new_subject.zoom_link
                    )
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
    return result.scalars()
