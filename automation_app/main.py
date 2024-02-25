from fastapi import FastAPI

from schedule.router import router_schedule

app = FastAPI(
    title='automation_bot'
)


app.include_router(
    router_schedule
)
