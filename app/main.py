from contextlib import asynccontextmanager
from fastapi import FastAPI

from .schedule.router import router_schedule
from .users.router import router_users

from .database import init_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    print("Приложение запущено")
    yield
    print("Приложение выключилось")


app = FastAPI(title="automation_bot", lifespan=lifespan)


app.include_router(router_schedule)
app.include_router(router_users)
