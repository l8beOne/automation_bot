import asyncio
import asyncpg
from utils.announcement_sender_list import SenderList
from middlewares.dbmiddleware import DbSession
import config
from aiogram import Bot, Dispatcher
from handlers import different_types, schedule, start_back, contacts, hse_info, announcement_sender
from utils import commands
from utils.redis_config import storage


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
    dp = Dispatcher(storage=storage)
    dp.update.middleware.register(DbSession(pool_connect))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # Регистрируем роутер для рассылки
    dp.include_router(announcement_sender.router)
    sender_list = SenderList(bot, pool_connect)

    # Регистрируем роутеры для кнопок с информацией
    dp.include_routers(schedule.router, start_back.router, contacts.router, hse_info.router, different_types.router)

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, senderlist=sender_list)
    

if __name__ == '__main__':
    asyncio.run(main())
