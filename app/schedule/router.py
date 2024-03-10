from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session, get_session
from ..schemas import ProgramSchema, ProgramBaseSchema
from .crud import (
    create_group_crud,
    create_program_crud,
    create_subject_crud,
    get_groups_crud,
    get_programs_crud,
    get_sepcific_schedule_crud,
    get_subjects_crud
)
from .schemas import (
    GroupBaseSchema,
    ScheduleBaseSchema,
    ScheduleSubjects,
    GroupSchema,
    SubjectBaseSchema,
    SubjectGetSchema
)


router_schedule = APIRouter(prefix="/schedule", tags=["Schedule"])
router_program = APIRouter(prefix="/program", tags=["Program"])
router_group = APIRouter(prefix="/group", tags=["Group"])
router_subject = APIRouter(prefix="/subject", tags=["Subject"])


@router_schedule.post("/")
async def create_schedule(
    new_schedule: ScheduleBaseSchema,
    db: AsyncSession = Depends(get_async_session)
):
    ...


@router_schedule.post("/subjects")
async def update_subjects():
    ...


@router_schedule.get("/{user_id}/{day}/", response_model=ScheduleSubjects)
async def get_specific_schedule(
    user_id: int,
    day: str,
    session: AsyncSession = Depends(get_async_session)
):
    result = await get_sepcific_schedule_crud(user_id, day, session)
    return result.all()


@router_program.post("/", response_model=ProgramSchema)
async def create_program(
    new_program: ProgramBaseSchema,
    session: AsyncSession = Depends(get_async_session),
    db: AsyncSession = Depends(get_session)
):
    result = await create_program_crud(new_program, session, db)
    return result.first()


@router_program.get("/", response_model=List[ProgramSchema])
async def get_programs(session: AsyncSession = Depends(get_session)):
    result = await get_programs_crud(session)
    return result.all()


@router_group.post("/", response_model=GroupSchema)
async def create_group(
    new_group: GroupBaseSchema,
    session: AsyncSession = Depends(get_async_session),
    db: AsyncSession = Depends(get_session)
):
    result = await create_group_crud(new_group, session, db)
    return result.first()


@router_group.get("/", response_model=List[GroupSchema])
async def get_groups(session: AsyncSession = Depends(get_session)):
    result = await get_groups_crud(session)
    return result.all()


@router_subject.post("/")
async def create_subject(
    new_subject: SubjectBaseSchema,
    session: AsyncSession = Depends(get_async_session)
):
    result = await create_subject_crud(new_subject, session)
    return result


@router_subject.get("/", response_model=List[SubjectGetSchema])
async def get_subjects(session: AsyncSession = Depends(get_session)):
    result = await get_subjects_crud(session)
    return result.all()
