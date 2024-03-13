from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas import ProgramSchema, ProgramBaseSchema
from .crud import (
    create_group_crud,
    create_program_crud,
    create_schedule_crud,
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


router = APIRouter(prefix="/schedule", tags=["Schedule"])


@router.post("/")
async def create_schedule(
    new_schedule: ScheduleBaseSchema,
    session: AsyncSession = Depends(get_db)
):
    result = await create_schedule_crud(new_schedule, session)
    if type(result) == dict and result.get("status") == "error":
        raise HTTPException(
            status_code=result.get("status_code"),
            detail=result.get("detail")
        )
    return result.first()


@router.post("/subjects")
async def update_subjects():
    ...


@router.get("/{user_id}/{day}/", response_model=ScheduleSubjects,)
async def get_specific_schedule(
    user_id: int,
    day: str,
    session: AsyncSession = Depends(get_db)
):
    result = await get_sepcific_schedule_crud(user_id, day, session)
    return result.all()


