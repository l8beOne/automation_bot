import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector
    

    async def check_table(self, table_name):
        query = f"SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = '{table_name}');"
        return await self.connector.fetchval(query)


    async def create_table(self, table_name):
        query = f"CREATE TABLE {table_name} (user_id bigint NOT NULL, status text, description text, PRIMARY KEY (user_id));"
        await self.connector.execute(query)
        query = f"INSERT INTO {table_name} (user_id, status, description) SELECT telegram_id, 'in_process', null FROM users;"
        await self.connector.execute(query)


    async def drop_table(self, table_name):
        query = f"DROP TABLE {table_name};"
        await self.connector.execute(query)
