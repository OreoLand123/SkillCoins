from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


button_balance = KeyboardButton("Баланс 💳")
button_get = KeyboardButton("Как заработать?")
button_buy = KeyboardButton("Потратить 💸")
button_back = KeyboardButton("На главную 🏠")
button_get_parser = InlineKeyboardButton("потратить 💎", callback_data="bt1")
button_yes = KeyboardButton("Да ✅")
batton_help = KeyboardButton("/start")
button_update = KeyboardButton("Обновить логи")


kb_mark = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_mark.row(button_get, button_balance, button_buy)

kb_mark_2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_mark_2.row(button_back)

kb_mark_3 = InlineKeyboardMarkup()
kb_mark_3.add(button_get_parser)

kb_mark_4 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_mark_4.row(button_yes, button_back)

kb_mark_5 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_mark_5.row(batton_help)

kb_mark_6 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_mark_6.row(button_update)