from create_bot import bot
import keyboard
from script import get_coins_info, buy_info, cheak_user_from, get_balans_user, sorted_list_of_awards, make_purchase


async def send_message_start(message):
    if cheak_user_from(str(message.from_user.id), message.from_user.username) == "0":
        await bot.send_message(message.from_user.id, "Ты кто?", reply_markup=keyboard.kb_mark_5)
    else:
        await bot.send_message(message.from_user.id, "Привет я TelegrammBot", reply_markup=keyboard.kb_mark)


async def send_message_balans(message):
    await bot.send_message(message.from_user.id, f"Баланс: {get_balans_user(str(message.from_user.id))} ", reply_markup=keyboard.kb_mark)


async def send_message_get(message):
    get_coins = get_coins_info()
    text = ""
    for i in get_coins:
        text += i + " : " + get_coins[i] + "\n\n"
    await bot.send_message(message.from_user.id, f"Как заработать: \n\n{text}", reply_markup=keyboard.kb_mark)


async def send_message_buy_info(message):
    buy_coins = sorted_list_of_awards()
    await bot.send_message(message.from_user.id, f"Варианты наград: ", reply_markup=keyboard.kb_mark_2)
    for i in buy_coins:
        await bot.send_message(message.from_user.id, f"{i} : {buy_coins[i]}", reply_markup=keyboard.kb_mark_3)


async def call_back(callback_query):
    cheak_ballans = get_balans_user(str(callback_query.message.chat.id))
    if cheak_ballans >= int(callback_query.message.text.split(" : ")[1]):
        await bot.send_message(callback_query.message.chat.id, f"Вы точно хотите потратить?", reply_markup=keyboard.kb_mark_4)
    else:
        await bot.send_message(callback_query.message.chat.id, "Недостаточно средств", reply_markup=keyboard.kb_mark)


async def send_message_back(message):
    await bot.send_message(message.from_user.id, "На главную", reply_markup=keyboard.kb_mark)


async def send_message_yes(message):
    await bot.send_message(message.from_user.id, f"Оплата прошла успешно", reply_markup=keyboard.kb_mark)
    


def register_handlers(dp):
    dp.register_message_handler(send_message_start, commands=["start"])
    dp.register_message_handler(send_message_balans, lambda message: "баланс" in message.text.lower(), state=None)
    dp.register_message_handler(send_message_get, lambda message: "как заработать" in message.text.lower(), state=None)
    dp.register_message_handler(send_message_buy_info, lambda message: "потратить" in message.text.lower(), state=None)
    dp.register_message_handler(send_message_back, lambda message: "на главную" in message.text.lower(), state=None)
    dp.register_callback_query_handler(call_back, lambda callback: callback.data == "bt1")
    dp.register_message_handler(send_message_yes, lambda message: "да" in message.text.lower(), state=None)
