from aiogram import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
TOKEN_BOT = None

bot = Bot(token=TOKEN_BOT)
dp = Dispatcher(bot, storage=storage)
