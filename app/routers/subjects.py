from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schedule.crud import create_subject_crud, get_subjects_crud
from ..schedule.schemas import SubjectBaseSchema, SubjectGetSchema


router = APIRouter(prefix="/subject", tags=["Subject"])


@router.post("/")
async def create_subject(
    new_subjects: List[SubjectBaseSchema],
    schedule_date: date,
    session: AsyncSession = Depends(get_db)
):
    result = await create_subject_crud(new_subjects, schedule_date, session)
    return result


@router.get("/", response_model=List[SubjectGetSchema])
async def get_subjects(session: AsyncSession = Depends(get_db)):
    result = await get_subjects_crud(session)
    return result.all()