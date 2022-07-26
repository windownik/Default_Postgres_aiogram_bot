from aiogram import types
from main import dp
from aiogram.dispatcher.filters import Text
import logging

from modules.funcs_handlers import reff_reg
from modules.sql_func import data_b
from modules.handlers.admin_handlers.download_users import upload_all_data, upload_all_users_id
from modules.dispatcher import bot, Admin
from aiogram.dispatcher import FSMContext
from modules.keyboards import start_user_kb, start_admin_kb


# Start menu
@dp.message_handler(commands=['start'], state='*')
async def start_menu(message: types.Message):
    # Обновляем данные пользователя в базе данных
    user_data = await data_b.read_by_name(id_data=message.from_user.id)

    if (str(user_data) == '[]' or str(user_data) == 'None') and 'reff' not in message.text:
        await data_b.insert_user(tg_id=message.from_user.id, name=message.from_user.first_name,
                                 nickname=message.from_user.username, language=message.from_user.language_code)
        await message.answer(text='🙎‍♂️🙍‍♀️ Давай определимся с полом', reply_markup=start_user_kb())

    elif (str(user_data) == '[]' or str(user_data) == 'None') and 'reff' in message.text:
        await reff_reg(message)
        await message.answer(text='🙎‍♂️🙍‍♀️ Давай определимся с полом', reply_markup=start_user_kb())

    elif user_data[0][4] == 'admin':
        await message.answer('Привет админ', reply_markup=start_admin_kb())
        await Admin.start.set()
    elif user_data[0][4] == 'close':
        await message.answer('🔙Главное меню')
        await data_b.update_db(table="all_users", name="status", data="active", id_data=message.from_user.id)
        await Admin.start.set()
    else:
        await message.answer('🔙Главное меню')


# Start menu
@dp.message_handler(commands=['create_db'], state='*')
async def start_menu(message: types.Message):
    # Создаем все таблицы в бд
    await data_b.create_fast_info_table()
    await data_b.reff_links_table()
    await data_b.all_users_table()
    await data_b.sender_table()
    await data_b.reff_table()
    await message.answer(text='Я создал все базы данных')


# Start menu
@dp.message_handler(commands=['i_am_admin'], state='*')
async def start_menu(message: types.Message):
    # Создаем все таблицы в бд
    await data_b.update_db(name='status', data='admin', id_data=message.from_user.id)
    await message.answer(text='Ты теперь админ')


# Cancel all process
@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await message.reply('Процес отменен. Все данные стерты. Что бы начать все с начала нажми /start',
                        reply_markup=types.ReplyKeyboardRemove())
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()


# Set admin
@dp.message_handler(commands=['id'], state='*')
async def start_menu(message: types.Message):
    await message.answer(f'Твой {message.from_user.id}\n'
                         f'Чат {message.chat.id}')


# Start menu
@dp.message_handler(active=True, state='*')
async def start_menu(message: types.Message):
    pass


# Get users
@dp.message_handler(commands=['get_all_users'], state='*')
async def start_menu(message: types.Message):
    await message.answer(f'Начал собирать файл')
    data = await data_b.read_all()
    number, bad = upload_all_data(data)
    await message.answer(f'Успешно {number}, ошибок {bad}\n\nЗагружаю')
    with open("all_users.xlsx", 'rb') as file:
        await bot.send_document(chat_id=message.from_user.id, document=file, caption="Все сделано!")


# Get users
@dp.message_handler(commands=['get_all_users_id'], state='*')
async def start_menu(message: types.Message):
    await message.answer(f'Начал собирать файл')
    data = await data_b.read_all()
    number, bad = upload_all_users_id(data)
    await message.answer(f'Успешно {number}, ошибок {bad}\n\nЗагружаю')
    with open("all_users.xlsx", 'rb') as file:
        await bot.send_document(chat_id=message.from_user.id, document=file, caption="Все сделано!")
