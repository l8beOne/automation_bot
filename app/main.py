from contextlib import asynccontextmanager
from fastapi import FastAPI

from .routers import groups, programs, subjects
from .schedule import router as schedules
from .users import router as users

from .database import init_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    print("Приложение запущено")
    yield
    print("Приложение выключилось")


app = FastAPI(title="automation_bot", lifespan=lifespan)


app.include_router(schedules.router)
app.include_router(users.router)
app.include_router(programs.router)
app.include_router(groups.router)
app.include_router(subjects.router)
