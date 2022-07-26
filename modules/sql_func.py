import asyncio
import asyncpg
import datetime

from modules.setings import MainSettings

constant = MainSettings()


# Создаем новую таблицу
class Database:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.cursor = loop.run_until_complete(
            asyncpg.create_pool(
                host=constant.db_host(),
                user=constant.user_db(),
                password=constant.password_db(),
                database=constant.db_name(),
                port=5432
            )
        )

    # Создаем новую таблицу
    async def all_users_table(self):
        await self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS all_users (
     id SERIAL PRIMARY KEY,
     tg_id BIGINT UNIQUE,
     user_name TEXT,
     nickname TEXT,
     status TEXT DEFAULT 'active',
     language TEXT DEFAULT 'ru',
     sex TEXT DEFAULT 'men',
     first_reg timestamp,
     activity timestamp)''')

    # Создаем новую таблицу
    async def create_fast_info_table(self):
        await self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS fast_info (
     id SERIAL PRIMARY KEY,
     tg_id BIGINT UNIQUE,
     data_1 TEXT,
     data_2 TEXT,
     data_3 TEXT,
     data_4 TEXT,
     data_5 TEXT)''')

    # Создаем новую таблицу
    async def sender_table(self):
        await self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS sender (
     id SERIAL PRIMARY KEY,
     tg_id BIGINT UNIQUE,
     text TEXT DEFAULT '0',
     media_type TEXT DEFAULT '0',
     media_id TEXT DEFAULT '0',
     k_board TEXT DEFAULT '0'
     )''')

    # Создаем новую таблицу
    async def reff_table(self):
        await self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS reff (
     id SERIAL PRIMARY KEY,
     tg_id BIGINT UNIQUE,
     mentor_tg_id BIGINT DEFAULT 0
     )''')

    # Создаем новую таблицу
    async def reff_links_table(self):
        await self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS reff_links (
     id SERIAL PRIMARY KEY,
     link BIGINT UNIQUE
     )''')

    async def insert_user(self, name: str, tg_id: str, nickname: str, language: str, table: str = 'all_users'):
        data_now = datetime.datetime.now()
        await self.cursor.execute(f"INSERT INTO {table} (tg_id, user_name, nickname, language, first_reg, activity) "
                                  f"VALUES ($1, $2, $3, $4, $5, $6) "
                                  f"ON CONFLICT DO NOTHING;", tg_id, name, nickname, language, data_now, data_now)

        await self.cursor.execute(f"INSERT INTO fast_info (tg_id) "
                                  f"VALUES ($1) "
                                  f"ON CONFLICT DO NOTHING;", tg_id)

    # Создаем новую таблицу
    async def insert_in_db(self, name: str, tg_id: str, data: str, table: str = 'all_users'):
        await self.cursor.execute(f"INSERT INTO {table} (tg_id, {name}) VALUES ($1, $2) "
                                  f"ON CONFLICT DO NOTHING;", tg_id, data)

    # Первая запись
    async def insert_reff(self, tg_id: str, mentor_tg_id: str):
        await self.cursor.execute(f"INSERT INTO reff (tg_id, mentor_tg_id) VALUES ($1, $2) "
                                  f"ON CONFLICT DO NOTHING;", tg_id, mentor_tg_id)

    # Первая запись
    async def insert_one(self, name: str, data: str, table: str = 'all_users'):
        await self.cursor.execute(f"INSERT INTO {table} ({name}) VALUES ($1) "
                                  f"ON CONFLICT DO NOTHING;", data)

    # Создаем новую таблицу
    async def update_db(self, data, name: str, id_data, id_name: str = 'tg_id', table: str = 'all_users'):
        await self.cursor.execute(f"UPDATE {table} SET {name}=($1) WHERE {id_name}=($2)", data, id_data)

    # Получаем все данные из таблицы
    async def read_all(self, name: str = '*', table: str = 'all_users'):
        return await self.cursor.fetch(f'SELECT {name} FROM {table}')

    # Счетаем количество
    async def count_all(self, table: str = 'all_users'):
        return await self.cursor.fetch(f'SELECT COUNT(*) FROM {table}')

    # Собираем все записи с фильтрацией по 1 параметру
    async def read_by_name(self, id_data, id_name: str = 'tg_id', name: str = '*', table: str = 'all_users'):
        return await self.cursor.fetch(f"SELECT {name} FROM {table} WHERE {id_name}=$1", id_data)

    # Собираем все записи с фильтрацией по интервалу дат
    async def read_all_by_date(self, days: int = 30, data_column: str = 'first_reg'):
        data_now = datetime.datetime.now()
        data_30 = data_now - datetime.timedelta(days=days)
        return await self.cursor.fetch(f"SELECT * FROM all_users WHERE {data_column} BETWEEN "
                                       f"$1::timestamp and "
                                       f"$2::timestamp order by id desc", data_30, data_now)

    # Собираем все записи с фильтрацией по 2 параметрам
    async def read_all_2(self, id_data, id_data2, id_name: str = 'tg_id', id_name2: str = 'tg_id',
                         name: str = '*', table: str = 'all_users'):
        return await self.cursor.fetch(f"SELECT {name} FROM {table} WHERE {id_name}=($1) AND {id_name2}=($2)", id_data,
                                       id_data2)

    # Собираем все записи с фильтрацией по 2 параметрам
    async def read_all_sender(self, id_data, id_name: str = 'tg_id',
                              name: str = '*', table: str = 'all_users'):
        return await self.cursor.fetch(f"SELECT {name} FROM {table} WHERE {id_name}=($1) AND status!='close'", id_data)

    # Удаляем строку в таблице
    async def delete_line_in_table(self, data, table: str = 'all_users', name: str = 'id'):
        await self.cursor.execute(f"DELETE FROM {table} WHERE {name}=$1", data)

    # Удаляем таблицу
    async def delete_table(self, table: str):
        await self.cursor.execute(f"DROP TABLE IF EXISTS {table}")


loop = asyncio.get_event_loop()
data_b = Database(loop)
