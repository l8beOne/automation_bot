import asyncio
import asyncpg
from utils.announcement_sender_list import SenderList
from middlewares.dbmiddleware import DbSession
from utils.announcement_state import Steps
import config
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, F
from handlers import different_types, schedule, start_back, contacts, hse_info, announcement_sender
from utils import commands
from filters.is_admin_filter import IsAdminFilter
from utils.redis_config import storage


async def start_bot(bot: Bot):
    await commands.set_commands(bot)
    await bot.send_message(config.ADMIN_ID, text="Бот запущен!")


async def stop_bot(bot: Bot):
    await bot.send_message(config.ADMIN_ID, text="Бот завершил работу!")


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
    dp = Dispatcher()
    dp.update.middleware.register(DbSession(pool_connect))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(announcement_sender.make_announce, Command(commands="announce"))
    dp.message.register(announcement_sender.get_announcement_message, Steps.get_announcement_message)
    dp.callback_query.register(announcement_sender.select_button, Steps.select_button)
    dp.message.register(announcement_sender.get_text_button, Steps.get_text_button)
    dp.message.register(announcement_sender.get_url, Steps.get_url)
    dp.callback_query.register(announcement_sender.send_process, F.data.in_(["confirm_announce", "cancel_announce"]))
    sender_list = SenderList(bot, pool_connect)
    # Регистрируем роутеры
    dp.include_routers(schedule.router, start_back.router, contacts.router, hse_info.router, different_types.router)
    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, senderlist=sender_list)
    

if __name__ == '__main__':
    asyncio.run(main())
