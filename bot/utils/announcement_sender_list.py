import asyncio
from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from aiogram.exceptions import TelegramRetryAfter
import asyncpg
from typing import List


class SenderList:
    def __init__(self, bot: Bot, connector: asyncpg.pool.Pool):
        self.bot = bot
        self.connector = connector
    
    async def get_inline_keyboard(self, button_text, button_url):
        builder = InlineKeyboardBuilder()
        builder.button(text=button_text, url=button_url)
        builder.adjust(1)
        return builder.as_markup()
    
    async def get_users_from_db(self, announce_name):
        async with self.connector.acquire() as connect:
            query = f"SELECT user_id FROM {announce_name} WHERE status = 'in_process';"
            query_results: List[asyncpg.Record] = await connect.fetch(query)
            return [result.get("user_id") for result in query_results]
    
    async def update_status(self, table_name, user_id, status, description):
        async with self.connector.acquire() as connect:
            query = f"UPDATE {table_name} SET status = '{status}', description = '{description}' WHERE user_id = {user_id};"
            await connect.execute(query)
    
    async def send_announce(self, user_id: int, from_chat_id: int, message_text: str, message_id: int, announce_name: str, keyboard: InlineKeyboardMarkup = None):
        try:
            await self.bot.send_message(user_id, message_text, reply_markup=keyboard)
        except TelegramRetryAfter as TooManyRequestsError:
            await asyncio.sleep(TooManyRequestsError.retry_after)
            return await self.send_announce(user_id, from_chat_id, message_id, announce_name, keyboard)
        except Exception as error:
            await self.update_status(announce_name, user_id, "unsuccessful", f"{error}")
        else:
            await self.update_status(announce_name, user_id, "success", "success")
            return True
        return False

    async def transmitter(self, announce_name: str, message_id: int, message_text: str, from_chat_id = int, button_text: str = None, button_url: str = None):
        keyboard = None
        if button_text and button_url:
            keyboard = await self.get_inline_keyboard(button_text, button_url)
        users_id = await self.get_users_from_db(announce_name)
        message_count = 0
        try:
            for user_id in users_id:
                if await self.send_announce(user_id, from_chat_id, message_text, message_id, announce_name, keyboard):
                    message_count += 1
                await asyncio.sleep(.05)
        finally:
            print(f"Сообщение разослано {message_count} пользователям")
        return message_count
