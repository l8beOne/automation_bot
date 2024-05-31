import asyncpg
from aiogram import Bot


class QuestionResponse:
    def __init__(self, bot: Bot, connector: asyncpg.pool.Pool):
        self.bot = bot
        self.connector = connector

    async def check_question_in_db(self, table_name, question):
        query = (
            f"SELECT EXISTS (SELECT question FROM {table_name} "
            f"WHERE question = '{question}');"
        )
        return await self.connector.fetchval(query)

    async def get_response_from_db(self, table_name, question):
        async with self.connector.acquire() as connect:
            query = (
                f"SELECT response FROM {table_name} "
                f"WHERE question = '{question}';"
            )
            query_result = await connect.fetch(query)
            response = str(query_result[0].get("response"))
            if response == "null":
                return (
                    "Данный вопрос уже находится на рассмотрении у "
                    "учебного офиса, ожидайте ответа"
                )
            return response

    async def add_question(
        self,
        table_name,
        user_id,
        question_id_in_chat,
        question
    ):
        async with self.connector.acquire() as connect:
            query = (
                f"INSERT INTO {table_name} "
                f"(user_id, question_id_in_chat, question, admin_id, "
                f"response, status) VALUES ({user_id}, "
                f"{question_id_in_chat}, '{question}', null, "
                f"'null', 'unexecuted');"
            )
            await connect.execute(query)

    async def get_user_id_for_reply(self, table_name, question):
        async with self.connector.acquire() as connect:
            query = (
                f"SELECT user_id FROM {table_name} "
                f"WHERE question = '{question}';"
            )
            query_result = await connect.fetch(query)
            user_id = int(query_result[0].get("user_id"))
            return user_id

    async def get_admin_id_dialog_unformed_answer(
        self, table_name, user_id
    ):
        async with self.connector.acquire() as connect:
            query = (
                f"SELECT admin_id FROM {table_name} "
                f"WHERE user_id = {user_id};"
            )
            query_result = await connect.fetch(query)
            admin_id = int(query_result[-1].get("admin_id"))
            return admin_id

    async def get_admin_id_dialog_formed_answer(
        self, table_name, question
    ):
        async with self.connector.acquire() as connect:
            query = (
                f"SELECT question_id, admin_id FROM {table_name} "
                f"WHERE question = '{question}';"
            )
            query_result = await connect.fetch(query)
            admin_id = int(query_result[0].get("admin_id"))
            question_id = int(query_result[0].get("question_id"))
            return question_id, admin_id

    async def get_question_from_db(self, table_name, question_id):
        async with self.connector.acquire() as connect:
            query = (
                f"SELECT question FROM {table_name} "
                f"WHERE question_id = {question_id};"
            )
            query_result = await connect.fetch(query)
            question = query_result[0].get("question")
            return question

    async def update_response_admin_id(
        self,
        table_name,
        question,
        response,
        admin_id
    ):
        async with self.connector.acquire() as connect:
            query = (
                f"UPDATE {table_name} SET response = '{response}', "
                f"admin_id = {admin_id}, status = 'executed' "
                f"WHERE question = '{question}';"
            )
            await connect.execute(query)
