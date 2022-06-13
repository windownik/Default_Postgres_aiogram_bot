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
def insert_user(name: str, tg_id: str, table: str = 'all_users'):
    connect = create_db_connect()
    data_now = datetime.datetime.now()
    try:
        with connect.cursor() as cursor:
            cursor.execute(f"INSERT INTO {table} (tg_id, user_name, status, first_reg, activity) "
                           f"VALUES (%s, %s, %s, %s, %s) "
                           f"ON CONFLICT DO NOTHING;", (tg_id, name, 'active', data_now, data_now))
            connect.commit()
            cursor.execute(f"INSERT INTO fast_info (tg_id) "
                           f"VALUES (%s) "
                           f"ON CONFLICT DO NOTHING;", (tg_id,))
            connect.commit()
    except Exception as _ex:
        print(_ex)
    finally:
        connect.close()


# Создаем новую таблицу
@connect_no_return
def insert_in_db(cursor, name: str, tg_id: str, data: str, table: str = 'all_users'):
    cursor.execute(f"INSERT INTO {table} (tg_id, {name}) VALUES (%s, %s) "
                   f"ON CONFLICT DO NOTHING;", (tg_id, data))


# Создаем новую таблицу
@connect_no_return
def update_db(cursor, data, name: str, id_data, id_name: str = 'tg_id', table: str = 'all_users'):
    cursor.execute(f"UPDATE {table} SET {name}=(%s) WHERE {id_name}=(%s)", (data, id_data))


# Получаем все данные из таблицы
@connect_with_return
def read_all(cursor, name: str = '*', table: str = 'all_users'):
    cursor.execute(f'SELECT {name} FROM {table}')


# Счетаем количество
@connect_with_return
def count_all(cursor, table: str = 'all_users'):
    cursor.execute(f'SELECT COUNT(*) FROM {table}')


# Собираем все записи с фильтрацией по 1 параметру
@connect_with_return
def read_by_name(cursor, id_data, id_name: str = 'tg_id', name: str = '*', table: str = 'all_users'):
    cursor.execute(f"SELECT {name} FROM {table} WHERE {id_name}=%s", (id_data,))


# Собираем все записи с фильтрацией по интервалу дат
@connect_with_return
def read_all_by_date(cursor, days: int = 30, data_column: str = 'first_reg'):
    data_now = datetime.datetime.now()
    data_30 = data_now - datetime.timedelta(days=days)
    cursor.execute(f"SELECT * FROM all_users WHERE {data_column} BETWEEN "
                   f"%s::timestamp and "
                   f"%s::timestamp order by id desc", (data_30, data_now))


# Собираем все записи с фильтрацией по 2 параметрам
@connect_with_return
def read_all_2(cursor, id_data, id_data2, id_name: str = 'tg_id', id_name2: str = 'tg_id',
               name: str = '*', table: str = 'all_users'):
    cursor.execute(f"SELECT {name} FROM {table} WHERE {id_name}=(%s) AND {id_name2}=(%s)", (id_data, id_data2))


# Удаляем строку в таблице
@connect_no_return
def delete_line_in_table(cursor, data, table: str = 'all_users', name: str = 'id'):
    cursor.execute(f"DELETE FROM {table} WHERE {name}=%s", (data,))


# Удаляем таблицу
@connect_no_return
def delete_table(cursor, table: str):
    cursor.execute(f"DROP TABLE IF EXISTS {table}")
