from aiogram import types

from main import dp
from modules.handlers.handlers_func import edit_text_call
from modules.sql_func import data_b


@dp.callback_query_handler(state='*')
async def start_menu(call: types.CallbackQuery):
    call_text = call.data
    if call_text == 'ru_lang':
        await edit_text_call(call, "Вы выбрали русский язык")
    elif call_text == 'en_lang':
        await data_b.update_db(name='language', data='en', id_data=call.from_user.id)
        await edit_text_call(call, "You pick english language")
