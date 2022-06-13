import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from modules.setings import MainSettings
from modules.my_filter import CheckActivityM


constant = MainSettings()
telegram_token = constant.tg_token()


storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(telegram_token)
dp = Dispatcher(bot, storage=storage)


# Включаем фильтры
dp.filters_factory.bind(CheckActivityM)


class Admin(StatesGroup):
    start = State()


class AdminSender(StatesGroup):
    new_text_post = State()
    new_media = State()
    new_k_board = State()
    choose_users = State()
    confirm_sender = State()


class UserWork(StatesGroup):
    pick_category = State()
    pick_market = State()
    cod_status = State()
    my_promo_cods = State()

    cod_feed_back = State()

    reg_premium_user = State()
    pick_category_premium = State()
    pick_market_premium = State()
    cod_status_premium = State()
