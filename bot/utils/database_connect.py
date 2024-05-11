import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector
    

    async def check_table(self, table_name):
        query = f"SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = '{table_name}');"
        return await self.connector.fetchval(query)


    async def create_announcement_table(self, table_name):
        query = f"CREATE TABLE {table_name} (user_id bigint NOT NULL, status text, description text, PRIMARY KEY (user_id));"
        await self.connector.execute(query)
        query = f"INSERT INTO {table_name} (user_id, status, description) SELECT telegram_id, 'in_process', null FROM users;"
        await self.connector.execute(query)


    async def create_question_response_table(self, table_name):
        query = f"CREATE TABLE {table_name} (user_id bigint NOT NULL, question_id bigint NOT NULL, question text, response text, status text, PRIMARY KEY (question));"
        await self.connector.execute(query)
    

    async def create_user_status_table(self, table_name):
        query = f"CREATE TABLE {table_name} (user_id bigint NOT NULL, user_status text, PRIMARY KEY (user_id));"
        await self.connector.execute(query)


    async def drop_announcement_table(self, table_name):
        query = f"DROP TABLE {table_name};"
        await self.connector.execute(query)
