from aiogram import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
TOKEN_BOT = "5584938260:AAGtikJ_6unrj8eimJebJdFR6WrF7cae-1Q"

bot = Bot(token=TOKEN_BOT)
dp = Dispatcher(bot, storage=storage)
