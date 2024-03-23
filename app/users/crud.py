from fastapi import HTTPException
from sqlalchemy import and_, any_, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Program, User, Group, GroupUsers
from ..schemas import ProgramName
from .schemas import UserCreateSchema


async def regisrtation_crud(
    new_user: UserCreateSchema,
    session: AsyncSession
):
    result = await session.execute(select(User).where(User.telegram_id == new_user.telegram_id))
    session_user = result.scalar()
    if session_user:
        return {
            "status": "error",
            "status_code": 400,
            "detail": "User already registered, "
                      "perhaps you want update"
        }
    stmt = insert(User).values(**new_user.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


async def get_users_crud(session: AsyncSession):
    qwery = select(User)
    result = await session.execute(qwery)
    return result.scalars()


async def regisrtation_with_program_crud(
    user_telegram_id: int,
    program_name: ProgramName,
    session: AsyncSession
):
    user_exists_qwery = await session.execute(select(User.id).where(User.telegram_id == user_telegram_id))
    user_id = user_exists_qwery.scalar()
    if not user_id:
        return {
            "status": "error",
            "status_code": 400,
            "detail": "No user with this telegram id"
        }
    program_result = await session.execute(select(Program.id).where(Program.name == program_name))
    program_id = program_result.scalar()
    if not program_id:
        return {
            "status": "error",
            "status_code": 400,
            "detail": "No program with this name"
        }
    await session.execute(
        update(User).where(
            User.telegram_id == user_telegram_id
        ).values(
            program_id=program_id
        )
    )
    await session.commit()
    user_result = await session.execute(
        select(
            User.name, Program.name
        ).where(
            User.telegram_id == user_telegram_id
        ).join(Program)
    )
    res = user_result.first()
    return {
        "status": "successfully added user to program",
        "data": {
            "user_name": res[0],
            "program_name": res[1]
        }
    }


async def registration_with_group_crud(
    user_telegram_id: int,
    group_name: str,
    session: AsyncSession,
):
    user_exists_qwery = await session.execute(select(User.id).where(User.telegram_id == user_telegram_id))
    user_id = user_exists_qwery.scalar()
    if not user_id:
        return {
            "status": "error",
            "status_code": 400,
            "detail": "No user with this telegram id"
        }
    group_result = await session.execute(select(Group.id).where(Group.name == group_name))
    group_id = group_result.scalar()
    if not group_id:
        return {
            "status": "error",
            "status_code": 400,
            "detail": "No group with this name"
        }
    group_names = await session.execute(select(Group.name).where(Group.users.any(id=user_id)))
    group_names_result = group_names.scalars()
    if group_name in group_names_result:
        return {
            "status": "error",
            "status_code": 400,
            "detail": "User already in this group"
        }

    await session.execute(insert(GroupUsers).values(group_id=group_id, users_id=user_id))
    await session.commit()

    group_names = await session.execute(select(Group.name).where(Group.users.any(id=user_id)))
    group_names_result = group_names.scalars()
    user = await session.execute(select(User.name).where(User.id == user_id))
    user_result = user.scalar()
    return {
        "status": "successfully added user to group",
        "data": {
            "user_name": user_result,
            "user_groups": [i for i in group_names_result]
        }
    }


async def get_user_crud(
    user_telegram_id: int,
    session: AsyncSession
):
    user = await session.execute(select(User).where(User.telegram_id == user_telegram_id).join(Program))
    result = user.scalars().first()
    if not result:
        return {
            "status": "error",
            "status_code": 404,
            "detail": "No user with this telegram_id"
        }
    return result
