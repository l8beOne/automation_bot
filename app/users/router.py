from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db, get_session
from ..schemas import UserGetSchema, UserProgramSchema, UserSchema, ProgramName
from .crud import (
    get_user_crud,
    get_users_crud,
    regisrtation_crud,
    regisrtation_with_program_crud,
    registration_with_group_crud
)
from .schemas import UserGroups, UserCreateSchema


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/auth")
async def regisrtation(
    new_user: UserCreateSchema,
    session: AsyncSession = Depends(get_db)
):
    return await regisrtation_crud(new_user, session)


@router.get("/", response_model=List[UserGetSchema])
async def get_users(session: AsyncSession = Depends(get_db)):
    result = await get_users_crud(session)
    return result.all()


@router.put("/auth/{user_id}/")# , response_model=UserSchema)
async def regisrtation_with_program(
    user_id: int, program_name: ProgramName,
    session: AsyncSession = Depends(get_db)
):
    result = await regisrtation_with_program_crud(
        user_id,
        program_name,
        session
    )
    return result# .first()


@router.post("/auth/{user_id}/")# , response_model=UserSchema)
async def regisrtation_with_group(
    user_id: int, group_name: str,
    session: AsyncSession = Depends(get_db),
):
    result = await registration_with_group_crud(
        user_id,
        group_name,
        session
    )
    if result.get("status") == "error":
        raise HTTPException(
            status_code=result.get("status_code"),
            detail=result.get("detail")
        )
    return result# .first()


@router.get("/{user_id}", response_model=UserGroups)
async def get_specific_user(
    user_id: int,
    session: AsyncSession = Depends(get_db)
):
    result = await get_user_crud(user_id, session)
    return result.first()
