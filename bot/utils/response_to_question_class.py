from aiogram import Bot
import asyncpg


class QuestionResponse:
    def __init__(self, bot: Bot, connector: asyncpg.pool.Pool):
        self.bot = bot
        self.connector = connector


    async def check_question_in_db(self, table_name, question):
        query = f"SELECT EXISTS (SELECT question FROM {table_name} WHERE question = '{question}');"
        return await self.connector.fetchval(query)


    async def get_response_from_db(self, table_name, question):
        async with self.connector.acquire() as connect:
            query = f"SELECT response FROM {table_name} WHERE question = '{question}';"
            query_result = await connect.fetch(query)
            response = str(query_result[0].get("response"))
            if response == "null":
                return "Данный вопрос уже находится на рассмотрении у учебного офиса, ожидайте ответа"
            return response


    async def add_question(self, table_name, user_id, question_id, question):
        async with self.connector.acquire() as connect:
            query = f"INSERT INTO {table_name} (user_id, question_id, question, response, status) VALUES ({user_id}, {question_id}, '{question}', 'null', 'unexecuted');"
            await connect.execute(query)


    async def get_user_id_for_reply(self, table_name, question):
        async with self.connector.acquire() as connect:
            query = f"SELECT user_id FROM {table_name} WHERE question = '{question}';"
            query_result = await connect.fetch(query)
            user_id = int(query_result[0].get("user_id"))
            return user_id


    async def update_response(self, table_name, question, response):
        async with self.connector.acquire() as connect:
            query = f"UPDATE {table_name} SET response = '{response}', status = 'executed' WHERE question = '{question}';"
            await connect.execute(query)
