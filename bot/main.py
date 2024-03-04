import asyncio
import config

from aiogram import Bot, Dispatcher
from handlers import different_types, schedule, start_back, contacts, hse_info


async def main():
    # Создаем объекты бота и диспетчера
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    # Регистрируем роутеры
    dp.include_routers(schedule.router, start_back.router, contacts.router, hse_info.router, different_types.router)
    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())
