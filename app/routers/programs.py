from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schedule.crud import create_program_crud, get_programs_crud
from ..schemas import ProgramBaseSchema, ProgramSchema


router = APIRouter(prefix="/program", tags=["Program"])


@router.post("/", response_model=ProgramSchema)
async def create_program(
    new_program: ProgramBaseSchema,
    session: AsyncSession = Depends(get_db)
):
    result = await create_program_crud(new_program, session)
    if type(result) == dict and result.get("status") == "error":
        raise HTTPException(
            status_code=result.get("status_code"),
            detail=result.get("detail")
        )
    return result.first()


@router.get("/", response_model=List[ProgramSchema])
async def get_programs(session: AsyncSession = Depends(get_db)):
    result = await get_programs_crud(session)
    return result.all()
