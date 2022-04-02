import datetime

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


# Новый юзер создает таблицу в бд
def all_users_table():
    global data_base
    try:
        data_base = create_db_connect()
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS all_users (
             id SERIAL PRIMARY KEY,
             tg_id BIGINT UNIQUE,
             user_name TEXT,
             status TEXT DEFAULT 'active',
             language TEXT DEFAULT 'ru',
             first_reg timestamp,
             activity timestamp)''')
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if data_base:
            data_base.close()


# Новый юзер создает таблицу в бд
def create_fast_info_table():
    global data_base
    try:
        data_base = create_db_connect()
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS fast_info (
             id SERIAL PRIMARY KEY,
             tg_id BIGINT UNIQUE,
             data_1 TEXT,
             data_2 TEXT,
             data_3 TEXT,
             data_4 TEXT,
             data_5 TEXT)''')
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if data_base:
            data_base.close()


# Админ создает таблицу для рассылки
def sender_table():
    global data_base
    try:
        data_base = create_db_connect()
        with data_base.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS sender (
             id SERIAL PRIMARY KEY,
             tg_id BIGINT UNIQUE,
             text TEXT DEFAULT '0',
             media_type TEXT DEFAULT '0',
             media_id TEXT DEFAULT '0',
             k_board TEXT DEFAULT '0'
             )''')
            data_base.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if data_base:
            data_base.close()


# Добавляем данные новому пользователю
def insert_user(name: str, tg_id: str, table: str = 'all_users'):
    global db
    data_now = datetime.datetime.now()
    try:
        db = create_db_connect()
        with db.cursor() as cursor:
            cursor.execute(f"INSERT INTO {table} (tg_id, user_name, status, first_reg, activity) "
                           f"VALUES (%s, %s, %s, %s, %s) "
                           f"ON CONFLICT DO NOTHING;", (tg_id, name, 'active', data_now, data_now))
            db.commit()
            cursor.execute(f"INSERT INTO fast_info (tg_id) "
                           f"VALUES (%s) "
                           f"ON CONFLICT DO NOTHING;", (tg_id,))
            db.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if db:
            db.close()


# Добавляем данные по соннику
def insert_in_db(name: str, tg_id: str, data: str, table: str = 'all_users'):
    global db
    try:
        db = create_db_connect()
        with db.cursor() as cursor:
            cursor.execute(f"INSERT INTO {table} (tg_id, {name}) VALUES (%s, %s) "
                           f"ON CONFLICT DO NOTHING;", (tg_id, data))
            db.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if db:
            db.close()


# Обновляем данные в базе данных
def update_db(data, name: str, id_data, id_name: str = 'tg_id', table: str = 'all_users'):
    try:
        db = create_db_connect()
        with db.cursor() as cursor:
            cursor.execute(f"UPDATE {table} SET {name}=(%s) WHERE {id_name}=(%s)", (data, id_data))
            db.commit()

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if db:
            db.close()


# Читаем все данные из базы данных
def read_all(
        name: str = '*',
        table: str = 'all_users'):
    global db
    try:

        db = create_db_connect()
        with db.cursor() as cursor:
            cursor.execute(f'SELECT {name} FROM {table}')
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if db:
            db.close()


# Читаем все данные из базы данных
def count_all(
        table: str = 'all_users'):
    global db
    try:
        db = create_db_connect()
        with db.cursor() as cursor:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if db:
            db.close()


# Собираем все записи с фильтрацией по 1 параметру
def read_by_name(
        id_data,
        id_name: str = 'tg_id',
        name: str = '*',
        table: str = 'all_users'):
    global db
    try:

        db = create_db_connect()
        with db.cursor() as cursor:
            cursor.execute(f"SELECT {name} FROM {table} WHERE {id_name}='{id_data}'")
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if db:
            db.close()


# Собираем все записи с фильтрацией по интервалу дат
def read_all_by_date(days: int = 30,
                     data_column: str = 'first_reg'):
    global db
    try:
        data_now = datetime.datetime.now()
        data_30 = data_now - datetime.timedelta(days=days)
        db = create_db_connect()
        with db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM all_users WHERE {data_column} between "
                           f"'{data_30}'::timestamp and "
                           f"'{data_now}'::timestamp order by id desc")
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if db:
            db.close()


# Собираем все записи с фильтрацией по 3 параметрам
def read_all_2(
        id_data,
        id_data2,
        id_name: str = 'tg_id',
        id_name2: str = 'tg_id',
        name: str = '*',
        table: str = 'all_users'):
    global db
    try:

        db = create_db_connect()
        with db.cursor() as cursor:
            cursor.execute(f"SELECT {name} FROM {table} WHERE {id_name}=(%s) AND {id_name2}=(%s)", (id_data, id_data2))
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if db:
            db.close()


# Удаляем строку в таблице
def delete_line_in_table(data, table: str = 'all_categorys', name: str = 'id'):
    global db
    try:
        db = create_db_connect()
        with db.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table} WHERE {name}='{data}'")
            db.commit()

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if db:
            db.close()


# Удаляем таблицу
def delete_table(table: str):
    global db
    try:
        db = create_db_connect()
        with db.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            db.commit()

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if db:
            db.close()
