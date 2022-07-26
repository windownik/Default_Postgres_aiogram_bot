from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


send_contact = KeyboardButton(text=f'📞Поделится контактом', request_contact=True)

send_contact_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(send_contact)


def start_user_kb():
    sex_female = InlineKeyboardButton(text='🙍‍♀️ Девушка', callback_data='sex_female')
    sex_men = InlineKeyboardButton(text='🙎‍♂️ Парень', callback_data='sex_men')
    start_kb = InlineKeyboardMarkup()
    start_kb.add(sex_men, sex_female)
    return start_kb


# клавиатура для админа стартовая
def back_kb_():
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    user_main = InlineKeyboardMarkup()
    return user_main.add(back)


def user_second_kb(cod_id=False):
    my_cod = InlineKeyboardButton(text='🛒 Мои промокоды', callback_data='my_cod')
    get_more_cod = InlineKeyboardButton(text='📝 Получить еще промокод!', callback_data='get_more_cod')
    if cod_id:
        bad_cod = InlineKeyboardButton(text='😢 Промокод не работает', callback_data=f'bad_cod{cod_id}')
    else:
        bad_cod = InlineKeyboardButton(text='😢 Промокод не работает', callback_data='bad_cod')
    start_kb = InlineKeyboardMarkup().add(my_cod)
    start_kb.add(get_more_cod)
    start_kb.add(bad_cod)
    return start_kb


def start_admin_kb():
    create_post = InlineKeyboardButton(text='📝 Разсылка 📝', callback_data='admin_sender')
    my_bot = InlineKeyboardButton(text='📊 Статистика пользователей 📊', callback_data='admin_stat')
    posts = InlineKeyboardButton(text='⚙️ Настройки ⚙️', callback_data='admin_setings')
    reff = InlineKeyboardButton(text='👥 Реферальные ссылки 👥', callback_data='admin_reff')
    inform = InlineKeyboardButton(text='👥 Зайти как user 👥', callback_data='admin_as_user')
    start_kb = InlineKeyboardMarkup().add(create_post)
    start_kb.add(my_bot)
    start_kb.add(posts)
    start_kb.add(inform)
    start_kb.add(reff)
    return start_kb


def special_reffs(without_list: bool = False):
    reff_list = InlineKeyboardButton(text='📝 список всех ID ссылок', callback_data='reff_list')
    check_reff_id = InlineKeyboardButton(text='📊 Получить статистику по рефф ID', callback_data='check_reff_id')
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    start_kb = InlineKeyboardMarkup()
    if not without_list:
        start_kb.add(reff_list)
    start_kb.add(check_reff_id)
    start_kb.add(back)
    return start_kb


# отправка в рассылке без медиа
def without_media():
    back = InlineKeyboardButton(text=f'Пропустить', callback_data=f'no_data')
    user_main = InlineKeyboardMarkup()
    user_main.add(back)
    return user_main


# клавиатура для админа стартовая
def confirm():
    yes_all_good = InlineKeyboardButton(text=f'Да все хорошо!', callback_data=f'yes_all_good')
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    user_main = InlineKeyboardMarkup()
    user_main.add(yes_all_good)
    user_main.add(back)
    return user_main


# клавиатура для админа стартовая
def choose_users():
    send_all = InlineKeyboardButton(text=f'Вообще всем', callback_data=f'send_all')
    send_en = InlineKeyboardButton(text=f'Всем парням', callback_data=f'send_men')
    send_ru = InlineKeyboardButton(text=f'Всем девушкам', callback_data=f'send_female')
    back = InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'back')
    user_main = InlineKeyboardMarkup()
    user_main.add(send_all)
    user_main.add(send_en)
    user_main.add(send_ru)
    user_main.add(back)
    return user_main


# Клавиатура для рассылки
def sender_kb(btns: str):
    btns = btns.split('\n')
    i = 0
    user_main = InlineKeyboardMarkup()
    while i <= len(btns) - 1:
        back = InlineKeyboardButton(text=btns[i], url=btns[i + 1])
        user_main.add(back)
        i += 2
    return user_main


# Клавиатура для категорий
def category_kb(category: dict = None):
    category_kb = InlineKeyboardMarkup()
    if category is None:
        pass
    else:
        for key in category.keys():
            btn = InlineKeyboardButton(text=category[key], callback_data=f'category_{key}')
            category_kb.add(btn)

    add_category = InlineKeyboardButton(text='➕ Добавить категорию.', callback_data='add_category')
    back = KeyboardButton(text='🔙 Назад', callback_data='category_back')

    category_kb.add(add_category)
    category_kb.add(back)
    return category_kb


# Клавиатура для под категорий
def podcategory_kb(index: int, category: dict = None):
    category_kb = InlineKeyboardMarkup()
    if category is None:
        pass
    else:
        for key in category.keys():
            btn = InlineKeyboardButton(text=category[key], callback_data=f'subcategory_{index}_{key}')
            category_kb.add(btn)

    add_category = InlineKeyboardButton(text='➕ Добавить подкатегорию.', callback_data=f'add_podcategory_{index}')
    correct_name = InlineKeyboardButton(text='✏️ Изменить название', callback_data=f'correct_name_{index}')
    delete_category = InlineKeyboardButton(text='❌ удалить эту категорию', callback_data=f'delete_category_{index}')
    back = KeyboardButton(text='🔙 Назад', callback_data=f'back_category')

    category_kb.add(add_category)
    category_kb.add(correct_name, delete_category)
    category_kb.add(back)
    return category_kb


# Клавиатура для под категорий
def confirm_kb(index):
    category_kb = InlineKeyboardMarkup()
    if index is None:
        confirm = InlineKeyboardButton(text='Да! Все верно!', callback_data=f'confirm')
        back = KeyboardButton(text='🔙 Назад', callback_data=f'back')
    else:
        confirm = InlineKeyboardButton(text='Да! Все верно!', callback_data=f'confirm_{index}')
        back = KeyboardButton(text='🔙 Назад', callback_data=f'backsub_{index}')

    category_kb.add(confirm, back)
    return category_kb

