from aiogram import Bot
import asyncpg


class UserStatusClass:
    def __init__(self, bot: Bot, connector: asyncpg.pool.Pool):
        self.bot = bot
        self.connector = connector

    
    async def add_user(self, table_name, user_id):
        async with self.connector.acquire() as connect:
            query = f"INSERT INTO {table_name} (user_id, user_status) VALUES ({user_id}, 'active');"
            await connect.execute(query)
    

    async def get_user_status(self, table_name, user_id):
        async with self.connector.acquire() as connect:
            query = f"SELECT user_status FROM {table_name} WHERE user_id = {user_id};"
            query_result = await connect.fetch(query)
            user_status = str(query_result[0].get("user_status"))
            return user_status
    

    async def update_user_status(self, table_name, user_id, user_status):
        async with self.connector.acquire() as connect:
            query = f"UPDATE {table_name} SET user_status = '{user_status}' WHERE user_id = {user_id};"
            await connect.execute(query)
