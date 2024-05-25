import asyncpg
from aiogram import Bot


class UserStatusClass:
    def __init__(self, bot: Bot, connector: asyncpg.pool.Pool):
        self.bot = bot
        self.connector = connector

    async def add_user(self, table_name, user_id):
        async with self.connector.acquire() as connect:
            query = (
                f"INSERT INTO {table_name} (user_id, full_name, user_status) "
                f"VALUES ({user_id}, 'null', 'active');"
            )
            await connect.execute(query)

    async def add_user_full_name(self, table_name, full_name, user_id):
        async with self.connector.acquire() as connect:
            query = (
                f"UPDATE {table_name} SET full_name = '{full_name}' "
                f"WHERE user_id = {user_id};"
            )
            await connect.execute(query)

    async def get_user_full_name(self, table_name, user_id):
        async with self.connector.acquire() as connect:
            query = (
                f"SELECT full_name FROM {table_name} "
                f"WHERE user_id = {user_id};"
            )
            query_result = await connect.fetch(query)
            user_full_name = str(query_result[0].get("full_name"))
            return user_full_name

    async def get_user_id(self, table_name, user_id):
        async with self.connector.acquire() as connect:
            query = (
                f"SELECT user_id FROM {table_name} "
                f"WHERE user_id = {user_id};"
            )
            query_result = await connect.fetch(query)
            user_id = int(query_result[0].get("user_id"))
            return user_id

    async def get_users_list(self, table_name):
        async with self.connector.acquire() as connect:
            query = f"SELECT user_id FROM {table_name};"
            query_result = await connect.fetch(query)
            users_list = []
            for item in query_result:
                user_id = int(item.get("user_id"))
                users_list.append(user_id)
            return users_list

    async def get_user_status(self, table_name, user_id):
        async with self.connector.acquire() as connect:
            query = (
                f"SELECT user_status FROM {table_name} WHERE "
                f"user_id = {user_id};"
            )
            query_result = await connect.fetch(query)
            user_status = str(query_result[0].get("user_status"))
            return user_status

    async def update_user_status(self, table_name, user_id, user_status):
        async with self.connector.acquire() as connect:
            query = (
                f"UPDATE {table_name} SET user_status = '{user_status}' "
                f"WHERE user_id = {user_id};"
            )
            await connect.execute(query)
