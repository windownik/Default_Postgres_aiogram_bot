import asyncio
import asyncpg
import datetime
from functools import wraps

import psycopg2

from modules.setings import MainSettings

constant = MainSettings()


def create_db_connect():
    data_base = psycopg2.connect(
        host=constant.db_host(),
        user=constant.user_db(),
        password=constant.password_db(),
        database=constant.db_name()
    )
    return data_base


def connect_no_return(func):
    """Decorator create/commit/close connection to database """

    @wraps(func)
    def _con(*args, **kwargs):
        connect = create_db_connect()
        cursor = connect.cursor()
        try:
            result = func(cursor, *args, **kwargs)
            connect.commit()
            return result
        except Exception as _ex:
            print(_ex)
        finally:
            connect.close()

    return _con


def connect_with_return(func):
    """Decorator create/commit/close connection to database """

    @wraps(func)
    def _con(*args, **kwargs):
        connect = create_db_connect()
        cursor = connect.cursor()
        try:
            func(cursor, *args, **kwargs)
            result = cursor.fetchall()
            return result
        except Exception as _ex:
            print(_ex)
        finally:
            connect.close()

    return _con


# Создаем новую таблицу
@connect_no_return
def all_users_table(cursor):
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS all_users (
     id SERIAL PRIMARY KEY,
     tg_id BIGINT UNIQUE,
     user_name TEXT,
     status TEXT DEFAULT 'active',
     language TEXT DEFAULT 'ru',
     first_reg timestamp,
     activity timestamp)''')


# Создаем новую таблицу
@connect_no_return
def create_fast_info_table(cursor):
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS fast_info (
     id SERIAL PRIMARY KEY,
     tg_id BIGINT UNIQUE,
     data_1 TEXT,
     data_2 TEXT,
     data_3 TEXT,
     data_4 TEXT,
     data_5 TEXT)''')


# Создаем новую таблицу
@connect_no_return
def sender_table(cursor):
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS sender (
     id SERIAL PRIMARY KEY,
     tg_id BIGINT UNIQUE,
     text TEXT DEFAULT '0',
     media_type TEXT DEFAULT '0',
     media_id TEXT DEFAULT '0',
     k_board TEXT DEFAULT '0'
     )''')


# Создаем новую таблицу
@connect_no_return
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

    async def insert_user(self, name: str, tg_id: str, table: str = 'all_users'):
        data_now = datetime.datetime.now()
        await self.cursor.execute(f"INSERT INTO {table} (tg_id, user_name, status, first_reg, activity) "
                                  f"VALUES ($1, $2, $3, $4, $5) "
                                  f"ON CONFLICT DO NOTHING;", tg_id, name, 'active', data_now, data_now)

        await self.cursor.execute(f"INSERT INTO fast_info (tg_id) "
                                  f"VALUES ($1) "
                                  f"ON CONFLICT DO NOTHING;", tg_id)

    # Создаем новую таблицу
    async def insert_in_db(self, name: str, tg_id: str, data: str, table: str = 'all_users'):
        await self.cursor.execute(f"INSERT INTO {table} (tg_id, {name}) VALUES ($1, $2) "
                                  f"ON CONFLICT DO NOTHING;", tg_id, data)

    # Создаем новую таблицу
    async def update_db(self, data, name: str, id_data, id_name: str = 'tg_id', table: str = 'all_users'):
        await self.cursor.execute(f"UPDATE {table} SET {name}=($1) WHERE {id_name}=($2)", data, id_data)

    # Получаем все данные из таблицы
    async def read_all(self, name: str = '*', table: str = 'all_users'):
        await self.cursor.fetch(f'SELECT {name} FROM {table}')

    # Счетаем количество
    async def count_all(self, table: str = 'all_users'):
        await self.cursor.fetch(f'SELECT COUNT(*) FROM {table}')

    # Собираем все записи с фильтрацией по 1 параметру
    async def read_by_name(self, id_data, id_name: str = 'tg_id', name: str = '*', table: str = 'all_users'):
        await self.cursor.fetch(f"SELECT {name} FROM {table} WHERE {id_name}=$1", id_data)

    # Собираем все записи с фильтрацией по интервалу дат
    async def read_all_by_date(self, days: int = 30, data_column: str = 'first_reg'):
        data_now = datetime.datetime.now()
        data_30 = data_now - datetime.timedelta(days=days)
        await self.cursor.fetch(f"SELECT * FROM all_users WHERE {data_column} BETWEEN "
                                f"$1::timestamp and "
                                f"$2::timestamp order by id desc", data_30, data_now)

    # Собираем все записи с фильтрацией по 2 параметрам
    async def read_all_2(self, id_data, id_data2, id_name: str = 'tg_id', id_name2: str = 'tg_id',
                         name: str = '*', table: str = 'all_users'):
        await self.cursor.fetch(f"SELECT {name} FROM {table} WHERE {id_name}=($1) AND {id_name2}=($2)", id_data,
                                id_data2)

    # Удаляем строку в таблице
    async def delete_line_in_table(self, data, table: str = 'all_users', name: str = 'id'):
        await self.cursor.execute(f"DELETE FROM {table} WHERE {name}=$1", data)

    # Удаляем таблицу
    async def delete_table(self, table: str):
        await self.cursor.execute(f"DROP TABLE IF EXISTS {table}")


loop = asyncio.get_event_loop()
data_b = Database(loop)
