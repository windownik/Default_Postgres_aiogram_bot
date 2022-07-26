from aiogram import types

from modules.sql_func import data_b
from modules.dispatcher import bot


async def reff_reg(message: types.Message):
    mentor_tg_id = message.text.split('reff')[1]
    if not mentor_tg_id.isdigit():

        await data_b.insert_user(nickname=message.from_user.username, tg_id=message.from_user.id,
                                 language=message.from_user.language_code, name=message.from_user.first_name)
        return
    mentor_tg_id = int(mentor_tg_id)
    user_data = await data_b.read_by_name(table='all_users', name='id', id_data=mentor_tg_id)

    if str(user_data) == '[]':
        await data_b.insert_one(table='reff_links', name='link', data=mentor_tg_id)
        await data_b.insert_reff(tg_id=message.from_user.id, mentor_tg_id=mentor_tg_id)
        await data_b.insert_user(nickname=message.from_user.username, tg_id=message.from_user.id,
                                 language=message.from_user.language_code, name=message.from_user.first_name)
        return
    await data_b.insert_reff(tg_id=message.from_user.id, mentor_tg_id=mentor_tg_id)
    await data_b.insert_user(nickname=message.from_user.username, tg_id=message.from_user.id,
                             language=message.from_user.language_code, name=message.from_user.first_name)
    await bot.send_message(text='✋ По вашей ссылке только что зарегистрировался пользователь.', chat_id=mentor_tg_id)
