from aiogram import types
from modules.handlers.handlers_func import edit_text_call
from main import dp
from modules.sql_func import count_all, read_all_by_date, read_by_name
from modules.dispatcher import Admin


# Create Text for statistic
def create_stat_text():
    all_users = count_all()[0][0]
    all_users_ru = len(read_by_name(name='id', id_name='language', id_data='ru'))
    all_users_en = len(read_by_name(name='id', id_name='language', id_data='en'))
    all_users_close = len(read_by_name(name='id', id_name='status', id_data='close'))
    all_new_users = len(read_all_by_date())
    active_users_7 = len(read_all_by_date(days=7, data_column='activity'))
    active_users_1 = len(read_all_by_date(days=1, data_column='activity'))
    text = f'👥Всего пользователей когда либо подписанных на бот: {all_users}\n' \
           f'❌Тех кто заблокировал бот: {all_users_close}\n' \
           f'👤Новых пользователей за 30 дней: {all_new_users}\n' \
           f'🙋‍♂️Активных пользователей за 7 дней: {active_users_7}\n' \
           f'🙋‍♂️Активных пользователей за 24 часа: {active_users_1}\n' \
           f'🇷🇺Русскоязычных пользователей: {all_users_ru}\n'\
           f'🇬🇧Англоязычных пользователей: {all_users_en}\n\n' \
           f'Для выхода /start'
    return text


@dp.callback_query_handler(state=Admin.start, text='admin_stat')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text=create_stat_text())
