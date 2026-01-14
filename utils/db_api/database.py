import asyncpg
from environs import Env

env = Env()
env.read_env()


class Database:
    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    # Connect to DB
    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD"),
            database=env.str("DB_NAME"),
            host=env.str("DB_HOST"),
            min_size=1,
            max_size=10,
        )
        print("✅ Connected to database")

    # Disconnect
    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    # Fetch multiple rows
    async def fetch(self, query: str, *args):
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]  # list of dict

    # Fetch single row
    async def fetchrow(self, query: str, *args):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None  # single dict

    # Execute query (INSERT, UPDATE, DELETE)
    async def execute(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    # Insert user
    async def insert_user(
        self,
        tg_id: int,
        first_name: str,
        phone_number: str | None = None
    ):
        query = """
        INSERT INTO users (tg_id, first_name, phone_number)
        VALUES ($1, $2, $3)
        ON CONFLICT (tg_id) DO NOTHING
        """
        async with self.pool.acquire() as conn:
            return await conn.execute(query, tg_id, first_name, phone_number)

    # Select user by tg_id
    async def select_user(self, tg_id: int) -> dict | None:
        query = "SELECT * FROM users WHERE tg_id = $1"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, tg_id)
            return dict(row) if row else None

    async def add_direct(self, name: str, contract: float):
        query = """
        INSERT INTO directions (name, contract) values ($1, $2)
                """
        async with self.pool.acquire() as conn:
            return await conn.execute(query, name, contract)

    async def select_directions(self) -> list[dict]:
        query = """
                SELECT id, name, contract
                FROM directions
                ORDER BY contract DESC \
                """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query)
            return rows

    async def add_test(self, question: str, answer: str):
        query = """
                INSERT INTO tests (question, answer)
                VALUES ($1, $2) \
                """
        async with self.pool.acquire() as conn:
            return await conn.execute(query, question, answer)


db = Database()