from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schedule.crud import create_group_crud, get_groups_crud
from ..schedule.schemas import GroupBaseSchema, GroupSchema


router = APIRouter(prefix="/group", tags=["Group"])


@router.post("/", response_model=GroupSchema)
async def create_group(
    new_group: GroupBaseSchema,
    session: AsyncSession = Depends(get_db),
    db: AsyncSession = Depends(get_db)
):
    result = await create_group_crud(new_group, session, db)
    if type(result) == dict and result.get("status") == "error":
        raise HTTPException(
            status_code=result.get("status_code"),
            detail=result.get("detail")
        )
    return result.first()


@router.get("/", response_model=List[GroupSchema])
async def get_groups(session: AsyncSession = Depends(get_db)):
    result = await get_groups_crud(session)
    return result.all()
