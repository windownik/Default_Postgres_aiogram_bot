from aiogram import executor
from modules.dispatcher import dp


if __name__ == '__main__':
    executor.start_polling(dp)
