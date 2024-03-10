from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session, get_session
from ..schemas import UserGetSchema, UserSchema, ProgramName
from .crud import (
    get_user_crud,
    get_users_crud,
    regisrtation_crud,
    regisrtation_with_program_crud
)
from .schemas import UserGroups, UserCreateSchema

router_users = APIRouter(prefix="/users", tags=["Users"])


@router_users.post("/auth")
async def regisrtation(
    new_user: UserCreateSchema,
    session: AsyncSession = Depends(get_async_session)
):
    return await regisrtation_crud(new_user, session)


@router_users.get("/", response_model=List[UserGetSchema])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await get_users_crud(session)
    return result.all()


@router_users.put("/auth/{user_id}/", response_model=UserSchema)
async def regisrtation_with_program(
    user_id: int, program_name: ProgramName,
    session: AsyncSession = Depends(get_async_session),
    db: AsyncSession = Depends(get_session)
):
    result = await regisrtation_with_program_crud(
        user_id,
        program_name,
        session, db
    )
    return result.first()


@router_users.get("/{user_id}", response_model=UserGroups)
async def get_specific_user(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    result = await get_user_crud(user_id, session)
    return result.first()
