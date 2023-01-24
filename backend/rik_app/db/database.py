from rik_app.models import Company
from rik_app.config import ConfigSingleton
from rik_app.tools.gentools import generate_companies
from rik_app.utils.classutils import SingletonMeta
from asyncpg.connection import Connection
from asyncpg.pool import Pool
from asyncpg import Record
from dotmap import DotMap
import asyncpg
import json


# -------------------------------------------------------------------------------- #
class DatabaseSingleton(metaclass=SingletonMeta):
    """
    This class is a singleton which contains a pool of connections
    to the backend Postgres database. Interactions with the database
    have been abstracted behind instance methods.
    """
    __conn_pool: Pool

    # ------------------------------------------------------------ #
    async def initialize(self) -> None:
        config = ConfigSingleton().postgres
        dbname = config.pop("database", None)
        conn: Connection = await asyncpg.connect(**config)
        exists = await self.__db_exists(conn, dbname)
        if not exists:
            await self.__create_db(conn, dbname)
        await conn.close()
        config.database = dbname
        self.__conn_pool = await asyncpg.create_pool(
            min_size=1,
            max_size=10,
            **config
        )
        if not exists:
            await self.__init_db()
            for company in generate_companies(300):
                await self.insert_company(company)

    # ------------------------------------------------------------ #
    @staticmethod
    async def __db_exists(conn: Connection, dbname: str) -> bool:
        query = "SELECT 1 FROM pg_database WHERE datname = $1"
        rows = await conn.fetch(query, dbname)
        return True if rows else False

    # ------------------------------------------------------------ #
    @staticmethod
    async def __create_db(conn: Connection, dbname: str) -> None:
        await conn.execute(f"CREATE DATABASE {dbname}")  # safe to inject value here

    # ------------------------------------------------------------ #
    async def __init_db(self) -> None:
        async with self.__conn_pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE companies (
                    name TEXT NOT NULL UNIQUE,
                    tin TEXT NOT NULL UNIQUE,
                    equity INTEGER NOT NULL,
                    founding_date DATE NOT NULL,
                    shareholders JSONB NOT NULL,
                    PRIMARY KEY (name, tin)
                );
                CREATE INDEX name_idx ON companies (name);
                CREATE INDEX tin_idx ON companies (tin);
            """)

    # ------------------------------------------------------------ #
    async def insert_company(self, company: Company) -> None:
        async with self.__conn_pool.acquire() as conn:
            query = """
                INSERT INTO companies 
                (name, tin, equity, founding_date, shareholders)
                VALUES ($1, $2, $3, $4, $5);
            """
            shds = company.to_dict()["shareholders"]
            await conn.execute(
                query,
                company.name,
                company.tin,
                company.equity,
                company.founding_date,
                json.dumps(shds)
            )

    # ------------------------------------------------------------ #
    async def update_company(self, company: Company) -> None:
        async with self.__conn_pool.acquire() as conn:
            query = """
                UPDATE companies
                SET equity = $1, shareholders = $2
                WHERE tin = $3
            """
            shds = company.to_dict()["shareholders"]
            await conn.execute(
                query,
                company.equity,
                json.dumps(shds),
                company.tin
            )

    # ------------------------------------------------------------ #
    async def fuzzy_find_companies_by_name(self, pattern: str) -> list:
        async with self.__conn_pool.acquire() as conn:
            query = "SELECT name, tin FROM companies WHERE name ILIKE $1"
            return await conn.fetch(query, f"%{pattern}%")

    # ------------------------------------------------------------ #
    async def fuzzy_find_companies_by_tin(self, tin: str) -> list:
        async with self.__conn_pool.acquire() as conn:
            query = "SELECT name, tin FROM companies WHERE tin ILIKE $1"
            return await conn.fetch(query, f"%{tin}%")

    # ------------------------------------------------------------ #
    async def get_company_details_by_tin(self, tin: str) -> Record | None:
        async with self.__conn_pool.acquire() as conn:
            query = "SELECT * FROM companies WHERE tin = $1"
            results = await conn.fetch(query, tin)
            return results[0] if results else None

    # ------------------------------------------------------------ #
    async def does_company_exist(self, tin) -> bool:
        async with self.__conn_pool.acquire() as conn:
            query = "SELECT EXISTS(SELECT 1 FROM companies WHERE tin = $1)"
            results = await conn.fetch(query, tin)
            return results[0]["exists"]
