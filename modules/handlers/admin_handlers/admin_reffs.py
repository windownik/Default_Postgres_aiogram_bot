from aiogram import types

from main import dp
from modules.dispatcher import Admin, AdminSpecialReff
from modules.handlers.handlers_func import edit_text_call
from modules.keyboards import special_reffs, confirm, back_kb_
from modules.sql_func import data_b


# Специальные рефералы
@dp.callback_query_handler(text='back', state=AdminSpecialReff.reff_list)
@dp.callback_query_handler(text='admin_reff', state=Admin.start)
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='👥 Специальные рефералы 👥\n\n'
                                         'Пример ссылки\n'
                                         'https://t.me/test_super_payment_bot?start=reff9115616', k_board=special_reffs())
    await AdminSpecialReff.start.set()


# Специальные рефералы список ID
@dp.callback_query_handler(text='back', state=AdminSpecialReff.get_stat)
@dp.callback_query_handler(text='reff_list', state=AdminSpecialReff.start)
async def start_menu(call: types.CallbackQuery):
    all_reff_id = await data_b.read_all(name='link', table='reff_links')
    if str(all_reff_id) == '[]':
        await edit_text_call(call=call, text='У вас нет ни одной реферальной ссылки', k_board=back_kb_())
        await AdminSpecialReff.reff_list.set()
        return
    await edit_text_call(call=call, text='Вот все твои id cсылок')
    # Create id's list
    text = ''
    for line in all_reff_id:
        text = text + f"<code>{line[0]}</code>\n"
    await call.message.answer(text=text, parse_mode='html', reply_markup=special_reffs(without_list=True))
    await AdminSpecialReff.reff_list.set()


# Специальные рефералы список ID
@dp.callback_query_handler(state=AdminSpecialReff.reff_list, text='check_reff_id')
@dp.callback_query_handler(state=AdminSpecialReff.start, text='check_reff_id')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='Введите рефф ID для проверки', k_board=back_kb_())
    await AdminSpecialReff.get_stat.set()


# Get all STAT inform for one reff link
@dp.message_handler(state=AdminSpecialReff.get_stat)
async def start_menu(message: types.Message):
    all_reff_id = await data_b.read_by_name(name='id', table='reff_links', id_name='link', id_data=int(message.text))
    if str(all_reff_id) == '[]':
        await message.answer('Данной ссылки нет в базе реферальных ссылок.')
        return
    all_reff_users = len(await data_b.read_by_name(name='id', table='reff', id_name='mentor_tg_id',
                                                   id_data=int(message.text)))
    text = f'👥 Всего подписалось по данной ссылке: <b>{all_reff_users}</b>\n'
    await message.answer(text=text, reply_markup=back_kb_(), parse_mode='html')
