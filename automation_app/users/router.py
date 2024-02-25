from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
import fastapi_users

from database import get_async_session
from models import User, Program, Group
from users.schemas import UserGroups
from schemas import UserCreateSchema, UserProgramCreateSchema, UserSchema


router_users = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router_users.post('/auth', response_model=UserSchema)
async def regisrtation(new_user: UserSchema, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(new_user).values(**new_user.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router_users.post('/auth/{user_id}/', response_model=UserSchema)
async def regisrtation_with_program(user_id: int, program_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(program_id=program_id)
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router_users.get('/{user_id}', response_model=UserGroups)
async def get_users(user_id: int, session: AsyncSession = Depends(get_async_session)):
    qwery = select(User).where(User.id == user_id)
    result = await session.execute(qwery)
    return result.all()
