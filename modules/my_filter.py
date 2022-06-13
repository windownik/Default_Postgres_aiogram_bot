
import datetime

from aiogram import types
from modules.sql_func import update_db
from aiogram.dispatcher.filters import BoundFilter


class CheckActivityM(BoundFilter):
    key = 'active'

    def __init__(self, active):
        self.active = active

    async def check(self, message: types.Message):
        try:
            now = datetime.datetime.now()
            update_db(table="all_users", name="activity", data=now, id_data=message.from_user.id)
            return False
        except Exception as _ex:
            print(_ex)
            return False
