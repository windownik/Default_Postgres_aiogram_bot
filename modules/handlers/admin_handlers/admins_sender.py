import datetime

from aiogram import types
from modules.handlers.handlers_func import edit_text_call
from main import dp
from modules.dispatcher import Admin, AdminSender
from modules.dispatcher import bot
from modules.keyboards import without_media, confirm, sender_kb, choose_users

# Рассылка  Первый экран
from modules.sql_func import data_b


@dp.callback_query_handler(text='back', state=AdminSender.choose_users)
@dp.callback_query_handler(text='admin_sender', state=Admin.start)
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='Отправьте мне сюда текст сообщения')
    await AdminSender.new_text_post.set()


# Рассылка Получаем фото либо пропускаем
@dp.message_handler(state=AdminSender.new_text_post)
async def start_menu(message: types.Message):
    # проверяем есть ли запись
    sender_data = await data_b.read_by_name(table='sender', id_data=message.from_user.id)
    if len(sender_data) == 0:
        await data_b.insert_in_db(table='sender', name='text', data=message.text, tg_id=message.from_user.id)
    else:
        await data_b.update_db(table='sender', name='text', data=message.text, id_data=message.from_user.id)
    await message.answer(text='Отправьте мне сюда фото, видео или документ',
                         reply_markup=without_media())
    await AdminSender.new_media.set()


# Рассылка Получаем файл. Запрос на кнопки
@dp.message_handler(state=AdminSender.new_media, content_types=types.ContentType.ANY)
async def start_menu(message: types.Message):
    await data_b.update_db(table='sender', name='media_type', data=message.content_type, id_data=message.from_user.id)
    if message.content_type == 'video':
        await data_b.update_db(table='sender', name='media_id', data=message.video.file_id,
                               id_data=message.from_user.id)
    elif message.content_type == 'audio':
        await data_b.update_db(table='sender', name='media_id', data=message.audio.file_id,
                               id_data=message.from_user.id)
    elif message.content_type == 'document':
        await data_b.update_db(table='sender', name='media_id', data=message.document.file_id,
                               id_data=message.from_user.id)
    elif message.content_type == 'animation':
        await data_b.update_db(table='sender', name='media_id', data=message.animation.file_id,
                               id_data=message.from_user.id)
    elif message.content_type == 'photo':
        await data_b.update_db(table='sender', name='media_id', data=message.photo[0].file_id,
                               id_data=message.from_user.id)
    else:
        await message.answer('Ошибка типа данных, попробуйте другой файл')
        return
    await message.answer(text=f'Отправьте мне сюда до трех кнопок в таком виде:\n'
                              f'Текст кнопки\n'
                              f'URL\n'
                              f'Текст кнопки\n'
                              f'URL',
                         reply_markup=without_media())
    await AdminSender.new_k_board.set()


# Рассылка. Пропускаем ввод медиа. Запрос на клавиатуру
@dp.callback_query_handler(state=AdminSender.new_media, text='no_data')
async def start_menu(call: types.CallbackQuery):
    await data_b.update_db(table='sender', name='media_type', data='text', id_data=call.from_user.id)
    await edit_text_call(call=call, text=f'Отправьте мне сюда до трех кнопок в таком виде:\n'
                                         f'Текст кнопки\n'
                                         f'URL\n'
                                         f'Текст кнопки\n'
                                         f'URL',
                         k_board=without_media())
    await AdminSender.new_k_board.set()


# Рассылка. Сохраняем все. Отправляем тестовое сообщение. Переход по кнопке без кнопок
@dp.callback_query_handler(state=AdminSender.new_k_board, text='no_data')
async def start_menu(call: types.CallbackQuery):
    await data_b.update_db(table='sender', name='k_board', data='0', id_data=call.from_user.id)
    send_data = (await data_b.read_by_name(table='sender', id_data=call.from_user.id))[0]
    type_msg = send_data[3]
    text_msg = send_data[2]
    media_id = send_data[4]
    if type_msg == 'photo':
        await bot.send_photo(chat_id=call.from_user.id, photo=media_id, caption=text_msg)
    elif type_msg == 'video':
        await bot.send_video(chat_id=call.from_user.id, video=media_id, caption=text_msg)
    elif type_msg == 'audio':
        await bot.send_audio(chat_id=call.from_user.id, audio=media_id, caption=text_msg)
    elif type_msg == 'animation':
        await bot.send_animation(chat_id=call.from_user.id, animation=media_id, caption=text_msg)
    elif type_msg == 'document':
        await bot.send_document(chat_id=call.from_user.id, document=media_id, caption=text_msg)
    elif type_msg == 'text':
        await bot.send_message(chat_id=call.from_user.id, text=text_msg)
    await call.message.answer('Данное сообщение будет отправленно в таком виде. Если все правильно подтвердите.',
                              reply_markup=confirm())
    await AdminSender.choose_users.set()


# Рассылка. Сохраняем все. Отправляем тестовое сообщение. С кнопками Нет валидации
@dp.message_handler(state=AdminSender.new_k_board)
async def start_menu(message: types.Message):
    await data_b.update_db(table='sender', name='k_board', data=message.text, id_data=message.from_user.id)
    if len(message.text.split('\n')) % 2 == 0:
        send_data = (await data_b.read_by_name(table='sender', id_data=message.from_user.id))[0]
        type_msg = send_data[3]
        text_msg = send_data[2]
        media_id = send_data[4]
        if type_msg == 'photo':
            await bot.send_photo(chat_id=message.from_user.id, photo=media_id, caption=text_msg,
                                 reply_markup=sender_kb(message.text))
        elif type_msg == 'video':
            await bot.send_video(chat_id=message.from_user.id, video=media_id, caption=text_msg,
                                 reply_markup=sender_kb(message.text))
        elif type_msg == 'audio':
            await bot.send_audio(chat_id=message.from_user.id, audio=media_id, caption=text_msg,
                                 reply_markup=sender_kb(message.text))
        elif type_msg == 'animation':
            await bot.send_animation(chat_id=message.from_user.id, animation=media_id, caption=text_msg,
                                     reply_markup=sender_kb(message.text))
        elif type_msg == 'document':
            await bot.send_document(chat_id=message.from_user.id, document=media_id, caption=text_msg,
                                    reply_markup=sender_kb(message.text))
        elif type_msg == 'text':
            await bot.send_message(chat_id=message.from_user.id, text=text_msg, reply_markup=sender_kb(message.text))
        await message.answer('Данное сообщение будет отправленно в таком виде. '
                             'Если все правильно подтвердите и перейдите к выбору типа пользователей.',
                             reply_markup=confirm())
        await AdminSender.choose_users.set()
    else:
        await message.answer('Не верно введены данные. Должно быть четное количество строк')


# Рассылка. Начинаем рассылку
@dp.callback_query_handler(state=AdminSender.choose_users, text='yes_all_good')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call,
                         text='Внимание после выбора кому отправлять сообщение рассылку нельзя будет остановить',
                         k_board=choose_users())
    await AdminSender.confirm_sender.set()


# Рассылка. Начинаем рассылку
@dp.callback_query_handler(state=AdminSender.confirm_sender)
async def start_menu(call: types.CallbackQuery):
    if call.data == 'send_men':
        all_users = await data_b.read_all_sender(id_name='sex', id_data='men', name='tg_id')
        key = 'Всем Парням'
    elif call.data == 'send_female':
        all_users = await data_b.read_all_sender(id_name='sex', id_data='female', name='tg_id')
        key = 'Всем Девушкам'
    else:
        all_users = await data_b.read_by_name(id_name='status!', id_data='close', name='tg_id')
        key = 'Вообще Всем'

    send_data = (await data_b.read_by_name(table='sender', id_data=call.from_user.id))[0]
    text_msg = send_data[2]
    type_msg = send_data[3]
    media_id = send_data[4]
    kb_data = send_data[5]
    good = 0
    bad = 0
    all_number = len(all_users)
    mess = await call.message.answer(f'<b>Рассылка: {key}</b>\n\n'
                                     '⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀ 0%\n\n'
                                     'Рассылка в работе\n'
                                     f'На момент запуска: {all_number}\n'
                                     f'✓ Успешно: 0\n'
                                     f'✕ Блокировали: 0\n'
                                     f'Скорость: ~/сек', parse_mode='html')
    start = datetime.datetime.now()
    try:
        for one_id in all_users:
            one_id = one_id[0]
            try:
                await send_for_all_users(type_msg=type_msg, kb_data=kb_data, one_id=one_id, text_msg=text_msg,
                                         media_id=media_id)
                good += 1
            except:
                await data_b.update_db(table="all_users", name="status", data="close", id_data=one_id)
                bad += 1
            await sender_text(good=good, bad=bad, all_number=all_number, mess_id=mess.message_id,
                              chat_id=call.message.chat.id, key=key, start=start)

        await bot.edit_message_text(text=f'<b>Рассылка: {key}</b>\n\n'
                                         '********** 100%\n\n'
                                         'Рассылка Завершена Успешно\n'
                                         f'На момент запуска: {all_number}\n'
                                         f'✓ Успешно: {good}\n'
                                         f'✕ Блокировали: {bad}\n'
                                         f'Скорость: {_speed(start, all_number)}/сек\n',
                                    chat_id=call.message.chat.id, message_id=mess.message_id, parse_mode='html')
    except:
        await bot.send_message(text=f'<b>Рассылка: {key}</b>\n\n'
                                    'Рассылка Прекращена аварийно!\n'
                                    f'На момент запуска: {all_number}\n'
                                    f'✓ Успешно: {good}\n'
                                    f'✕ Блокировали: {bad}\n',
                               chat_id=call.message.chat.id, parse_mode='html')


# Отправляем сообщение для каждого пользователя
async def send_for_all_users(type_msg: str, kb_data, one_id: int, text_msg: str, media_id: str):
    if type_msg == 'photo':
        if kb_data == '0':
            await bot.send_photo(chat_id=one_id, photo=media_id, caption=text_msg)
        else:
            await bot.send_photo(chat_id=one_id, photo=media_id, caption=text_msg,
                                 reply_markup=sender_kb(kb_data))
    elif type_msg == 'video':
        if kb_data == '0':
            await bot.send_video(chat_id=one_id, video=media_id, caption=text_msg)
        else:
            await bot.send_video(chat_id=one_id, video=media_id, caption=text_msg,
                                 reply_markup=sender_kb(kb_data))
    elif type_msg == 'audio':
        if kb_data == '0':
            await bot.send_audio(chat_id=one_id, audio=media_id, caption=text_msg)
        else:
            await bot.send_audio(chat_id=one_id, audio=media_id, caption=text_msg,
                                 reply_markup=sender_kb(kb_data))
    elif type_msg == 'animation':
        if kb_data == '0':
            await bot.send_animation(chat_id=one_id, animation=media_id, caption=text_msg)
        else:
            await bot.send_animation(chat_id=one_id, animation=media_id, caption=text_msg,
                                     reply_markup=sender_kb(kb_data))
    elif type_msg == 'document':
        if kb_data == '0':
            await bot.send_document(chat_id=one_id, document=media_id, caption=text_msg)
        else:
            await bot.send_document(chat_id=one_id, document=media_id, caption=text_msg,
                                    reply_markup=sender_kb(kb_data))
    elif type_msg == 'text':
        if kb_data == '0':
            await bot.send_message(chat_id=one_id, text=text_msg)
        else:
            await bot.send_message(chat_id=one_id, text=text_msg, reply_markup=sender_kb(kb_data))


async def sender_text(good: int, bad: int, all_number: int, mess_id: int, chat_id: int, key: str,
                      start: datetime.datetime):
    send_number = good + bad
    if all_number < 3000:
        if int(all_number / 2) == send_number:
            await bot.edit_message_text(text=f'<b>Рассылка: {key}</b>\n\n'
                                             '*****⣀⣀⣀⣀⣀ 50%\n\n'
                                             'Рассылка в работе\n'
                                             f'На момент запуска: {all_number}\n'
                                             f'✓ Успешно: {good}\n'
                                             f'✕ Блокировали: {bad}\n'
                                             f'Скорость: {_speed(start, send_number)}/сек\n',
                                        chat_id=chat_id, message_id=mess_id, parse_mode='html')
        elif all_number == send_number:
            await bot.edit_message_text(text=f'<b>Рассылка: {key}</b>\n\n'
                                             '********** 100%\n\n'
                                             'Рассылка в работе\n'
                                             f'На момент запуска: {all_number}\n'
                                             f'✓ Успешно: {good}\n'
                                             f'✕ Блокировали: {bad}\n'
                                             f'Скорость: {_speed(start, send_number)}/сек\n',
                                        chat_id=chat_id, message_id=mess_id, parse_mode='html')

    if send_number % 500 == 0:
        text = f'<b>Рассылка: {key}</b>\n\n' \
               f'{_percent(all_number=all_number, now_number=send_number)}%\n\n' \
               'Рассылка в работе\n' \
               f'На момент запуска: {all_number}\n' \
               f'✓ Успешно: {good}\n' \
               f'✕ Блокировали: {bad}\n' \
               f'Скорость: {_speed(start, send_number)}/сек\n'
        try:
            await bot.edit_message_text(text=text, chat_id=chat_id, parse_mode='html',
                                        message_id=mess_id)
        except Exception as _ex:
            print(text)
            print('MORE 3000 ERROR  ', _ex)


def delta_hours(start: datetime.datetime) -> str:
    duration = datetime.datetime.now() - start
    seconds = duration.seconds
    hours = seconds // 3600
    duration = seconds % 3600
    minutes = duration // 60
    return f'~{hours} ч.{minutes}мин.'


def _speed(start: datetime.datetime, now_number: int) -> int:
    duration = datetime.datetime.now() - start
    seconds = duration.seconds
    if seconds == 0:
        seconds = 1
    speed = now_number // seconds
    return speed


def _percent(all_number: int, now_number: int) -> str:
    percent = int((now_number * 100) // all_number)
    graph = int(percent // 10) * '*'
    blank = (10 - int(percent / 10)) * '⣀'
    return f'{graph}{blank} {percent}'
