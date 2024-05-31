import asyncio

import asyncpg
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
from handlers import (
    announcement_sender,
    certificate,
    contacts,
    different_types,
    hse_info,
    mute,
    response_to_question,
    schedule,
    start_back,
)
# from handlers.schedule_tracking import (
#     check_for_updates,
#     compare_prev_current_schedule_results,
# )
from middlewares.apschedulermiddleware import SchedulerMiddleware
from middlewares.dbmiddleware import DbSession
from utils import commands
from utils.announcement_sender_list import SenderList
# from utils.database_connect import Request
from utils.redis_config import storage
from utils.response_to_question_class import QuestionResponse
from utils.user_status_class import UserStatusClass


async def start_bot(bot: Bot):
    await commands.set_commands(bot)
    for admin_id in config.ADMIN_IDS:
        await bot.send_message(admin_id, text="Бот запущен!")


async def stop_bot(bot: Bot):
    for admin_id in config.ADMIN_IDS:
        await bot.send_message(admin_id, text="Бот завершил работу!")


async def create_pool():
    return await asyncpg.create_pool(
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        database=config.POSTGRES_DB,
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
    )


async def main():
    # Создаем объекты бота и диспетчера
    bot = Bot(token=config.BOT_TOKEN)
    pool_connect = await create_pool()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    dp = Dispatcher(storage=storage)
    dp.update.middleware.register(DbSession(pool_connect))
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # Регистрируем роутер для рассылки
    dp.include_router(announcement_sender.router)
    sender_list = SenderList(bot, pool_connect)
    question_response = QuestionResponse(bot, pool_connect)
    users_status = UserStatusClass(bot, pool_connect)
    # request = Request(pool_connect)

    # Вставить эту функцию при выборе пользователем его ОП и курса
    # start_schedule_data = check_for_updates(config.SCHEDULE_PARAMS)
    # await compare_prev_current_schedule_results(
    #     bot,
    #     start_schedule_data,
    #     users_status,
    #     scheduler,
    #     request,
    #     sender_list
    # )

    scheduler.start()

    # Регистрируем роутеры для кнопок с информацией
    dp.include_routers(
        schedule.router,
        start_back.router,
        certificate.router,
        contacts.router,
        hse_info.router,
        mute.router,
        response_to_question.router,
        different_types.router,
    )

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        senderlist=sender_list,
        questionresponse=question_response,
        userstatus=users_status,
    )


if __name__ == "__main__":
    asyncio.run(main())
