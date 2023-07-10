from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from datetime import datetime
from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None
        self.now = datetime.now()

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO main_user (full_name, username, telegram_id, created, updated) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, full_name, username, telegram_id, self.now, self.now, fetchrow=True)

    async def add_fileid(self, title, file_id, show=True):
        sql = "INSERT INTO main_fileid (title, file_id, show, created, updated) VALUES ($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, title, file_id, show, self.now, self.now, fetchrow=True)

    async def add_keyword(self, content, file_id):
        sql = "INSERT INTO main_keyword (content, file_id, created, updated) VALUES ($1, $2, $3, $4) returning *"
        return await self.execute(sql, content, file_id, self.now, self.now, fetchrow=True)

    async def add_audio(self, link, file_id, caption):
        sql = "INSERT INTO main_audio (link, file_id, caption) VALUES ($1, $2, $3) returning *"
        return await self.execute(sql, link, file_id, caption, fetchrow=True)

    async def select_all_keywords(self):
        sql = """SELECT content FROM main_keyword"""
        return await self.execute(sql, fetch=True)

    async def select_all_categories(self):
        sql = "SELECT * FROM main_category"
        return await self.execute(sql, fetch=True)

    async def get_cat(self, **kwargs):
        sql = "SELECT * FROM main_category WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_all_fileids(self, **kwargs):
        sql = "SELECT * FROM main_fileid WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def get_files_by_keyword(self, **kwargs):
        sql = """SELECT * FROM main_keyword WHERE """
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def get_fileids(self, **kwargs):
        sql = "SELECT * FROM main_fileid WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_all_fileid(self):
        sql = "SELECT file_id FROM main_fileid"
        return await self.execute(sql, fetch=True)

    async def select_file(self, **kwargs):
        sql = "SELECT * FROM main_fileid WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_audio(self, **kwargs):
        sql = "SELECT * FROM main_audio WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM main_user"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM main_user WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM main_user"
        return await self.execute(sql, fetchval=True)
    
    async def count_musics(self):
        sql = "SELECT COUNT(*) FROM main_fileid"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE main_user SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM main_user WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE main_user", execute=True)
