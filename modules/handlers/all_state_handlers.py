from aiogram import types

from main import dp
from modules.handlers.handlers_func import edit_text_call
from modules.sql_func import data_b


@dp.callback_query_handler(state='*')
async def start_menu(call: types.CallbackQuery):
    call_text = call.data
    if call_text == 'sex_female':
        await data_b.update_db(name='sex', data='female', id_data=call.from_user.id)
    elif call_text == 'sex_men':
        await data_b.update_db(name='sex', data='men', id_data=call.from_user.id)
    await edit_text_call(call, "Отлично")
