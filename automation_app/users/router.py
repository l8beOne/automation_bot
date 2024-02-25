from fastapi import APIRouter


router_users = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router_users.post('/auth')
async def regisrtation(*args, **kwargs):
    return


@router_users.get('/{user_id}')
async def get_users(*args, **kwargs):
    return
