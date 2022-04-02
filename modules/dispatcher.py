from aiogram import Bot, Dispatcher
from modules.setings import MainSettings
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

import logging

constant = MainSettings()
telegram_token = constant.tg_token()


storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(telegram_token)
dp = Dispatcher(bot, storage=storage)


class Admin(StatesGroup):
    start = State()


class Admin_sender(StatesGroup):
    new_text_post = State()
    new_media = State()
    new_k_board = State()
    choose_users = State()
    confirm_sender = State()


class User_Work(StatesGroup):
    pick_category = State()
    pick_market = State()
    cod_status = State()
    my_promo_cods = State()

    cod_feed_back = State()

    reg_premium_user = State()
    pick_category_premium = State()
    pick_market_premium = State()
    cod_status_premium = State()
