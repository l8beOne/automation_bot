from fastapi import HTTPException
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Program, User
from ..schemas import ProgramName
from .schemas import UserCreateSchema


async def regisrtation_crud(
    new_user: UserCreateSchema,
    session: AsyncSession
):
    stmt = insert(User).values(**new_user.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


async def get_users_crud(session: AsyncSession):
    qwery = select(User)
    result = await session.execute(qwery)
    return result


async def regisrtation_with_program_crud(
    user_id: int,
    program_name: ProgramName,
    session: AsyncSession,
    db: AsyncSession
):
    program_qwery = select(Program).where(Program.name == program_name)
    program_result = await db.execute(program_qwery)
    program_id = program_result.scalar()
    print(program_id)
    if not program_id:
        raise HTTPException(
            status_code=400,
            detail="No program with this name"
        )
    stmt = update(User).where(User.id == user_id).values(program_id=program_id)
    await session.execute(stmt)
    await session.commit()
    # проблемы начинаются тут
    user_qwery = select(User).where(User.id == user_id).join(Program)
    user_result = await db.execute(user_qwery)
    return user_result


async def get_user_crud(
    user_id: int,
    session: AsyncSession
):
    qwery = select(User).where(User.id == user_id).join(Program)
    result = await session.execute(qwery)
    return result
