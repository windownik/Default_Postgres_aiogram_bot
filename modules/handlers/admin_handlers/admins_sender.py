from aiogram import types
from modules.handlers.handlers_func import edit_text_call
from main import dp
from modules.sql_func import insert_in_db, update_db, read_by_name, read_all_2
from modules.dispatcher import Admin, Admin_sender
from modules.dispatcher import bot
from modules.keyboards import without_media, confirm, sender_kb, choose_users


# Рассылка  Первый экран
@dp.callback_query_handler(text='back', state=Admin_sender.choose_users)
@dp.callback_query_handler(text='admin_sender', state=Admin.start)
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call, text='Отправьте мне сюда текст сообщения')
    await Admin_sender.new_text_post.set()


# Рассылка Получаем фото либо пропускаем
@dp.message_handler(state=Admin_sender.new_text_post)
async def start_menu(message: types.Message):
    # проверяем есть ли запись
    sender_data = read_by_name(table='sender', id_data=message.from_user.id)
    if len(sender_data) == 0:
        insert_in_db(table='sender', name='text', data=message.text, tg_id=message.from_user.id)
    else:
        update_db(table='sender', name='text', data=message.text, id_data=message.from_user.id)
    await message.answer(text='Отправьте мне сюда фото, видео или документ',
                         reply_markup=without_media())
    await Admin_sender.new_media.set()


# Рассылка Получаем файл. Запрос на кнопки
@dp.message_handler(state=Admin_sender.new_media, content_types=types.ContentType.ANY)
async def start_menu(message: types.Message):
    update_db(table='sender', name='media_type', data=message.content_type, id_data=message.from_user.id)
    if message.content_type == 'video':
        update_db(table='sender', name='media_id', data=message.video.file_id, id_data=message.from_user.id)
    elif message.content_type == 'audio':
        update_db(table='sender', name='media_id', data=message.audio.file_id, id_data=message.from_user.id)
    elif message.content_type == 'document':
        update_db(table='sender', name='media_id', data=message.document.file_id,
                  id_data=message.from_user.id)
    elif message.content_type == 'animation':
        update_db(table='sender', name='media_id', data=message.animation.file_id,
                  id_data=message.from_user.id)
    elif message.content_type == 'photo':
        update_db(table='sender', name='media_id', data=message.photo[0].file_id,
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
    await Admin_sender.new_k_board.set()


# Рассылка. Пропускаем ввод медиа. Запрос на клавиатуру
@dp.callback_query_handler(state=Admin_sender.new_media, text='no_data')
async def start_menu(call: types.CallbackQuery):
    update_db(table='sender', name='media_type', data='text', id_data=call.from_user.id)
    await edit_text_call(call=call, text=f'Отправьте мне сюда до трех кнопок в таком виде:\n'
                                         f'Текст кнопки\n'
                                         f'URL\n'
                                         f'Текст кнопки\n'
                                         f'URL',
                         k_board=without_media())
    await Admin_sender.new_k_board.set()


# Рассылка. Сохраняем все. Отправляем тестовое сообщение. Переход по кнопке без кнопок
@dp.callback_query_handler(state=Admin_sender.new_k_board, text='no_data')
async def start_menu(call: types.CallbackQuery):
    update_db(table='sender', name='k_board', data='0', id_data=call.from_user.id)
    send_data = read_by_name(table='sender', id_data=call.from_user.id)[0]
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
    await Admin_sender.choose_users.set()


# Рассылка. Сохраняем все. Отправляем тестовое сообщение. С кнопками Нет валидации
@dp.message_handler(state=Admin_sender.new_k_board)
async def start_menu(message: types.Message):
    update_db(table='sender', name='k_board', data=message.text, id_data=message.from_user.id)
    if len(message.text.split('\n')) % 2 == 0:
        send_data = read_by_name(table='sender', id_data=message.from_user.id)[0]
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
        await Admin_sender.choose_users.set()
    else:
        await message.answer('Не верно введены данные. Должно быть четное количество строк')


# Рассылка. Начинаем рассылку
@dp.callback_query_handler(state=Admin_sender.choose_users, text='yes_all_good')
async def start_menu(call: types.CallbackQuery):
    await edit_text_call(call=call,
                         text='Внимание после выбора кому отправлять сообщение рассылку нельзя будет остановить',
                         k_board=choose_users())
    await Admin_sender.confirm_sender.set()


# Рассылка. Начинаем рассылку
@dp.callback_query_handler(state=Admin_sender.confirm_sender)
async def start_menu(call: types.CallbackQuery):
    if call.data == 'send_ru':
        all_users = read_all_2(name='tg_id', id_name='status', id_data='active', id_name2='language', id_data2='ru')
    elif call.data == 'send_en':
        all_users = read_all_2(name='tg_id', id_name='status', id_data='active', id_name2='language', id_data2='en')
    else:
        all_users = read_by_name(name='tg_id', id_name='status', id_data='active')

    await call.message.answer('Начинаю рассылку')
    send_data = read_by_name(table='sender', id_data=call.from_user.id)[0]
    text_msg = send_data[2]
    type_msg = send_data[3]
    media_id = send_data[4]
    kb_data = send_data[5]
    good = 0
    bad = 0
    for one_id in all_users:
        one_id = one_id[0]
        try:
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
            good += 1
        except Exception as _ex:
            update_db(table="all_users", name="status", data="close", id_data=one_id)
            bad += 1
    await call.message.answer(f'Закончил рассылку\n'
                              f'успешно: {good}\n'
                              f'неудачно: {bad}')
