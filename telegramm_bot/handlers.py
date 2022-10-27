from create_bot import bot
import keyboard
from script import get_coins_info, get_balans_user, get_list_of_awards, make_purchase, check_user_id
from States import FSMAdmin, FSMContext

ID = []

async def send_message_start(message):
    if not check_user_id(str(message.from_user.id), message.from_user.username, ID):
        await bot.send_message(message.from_user.id, "Ты кто?", reply_markup=keyboard.kb_mark_5)
    else:
        await bot.send_message(message.from_user.id, f"Привет я TelegramBot", reply_markup=keyboard.kb_mark)

async def send_message_balans(message):
    if str(message.from_user.id) in ID:
        await bot.send_message(message.from_user.id, f"Баланс: {get_balans_user(str(message.from_user.id))} ", reply_markup=keyboard.kb_mark)

async def send_message_get(message):
    if str(message.from_user.id) in ID:
        get_coins = get_coins_info()
        text = ""
        for i in get_coins:
            text += i + " : " + get_coins[i] + "\n\n"
        await bot.send_message(message.from_user.id, f"Как заработать: \n\n{text}", reply_markup=keyboard.kb_mark)

async def send_message_buy_info(message):
    if str(message.from_user.id) in ID:
        list_of_awards = get_list_of_awards()
        await FSMAdmin.reason.set()
        await bot.send_message(message.from_user.id, f"Варианты наград: ", reply_markup=keyboard.kb_mark_2)
        for i in list_of_awards:
            await bot.send_message(message.from_user.id, f"{i} : {list_of_awards[i]}", reply_markup=keyboard.kb_mark_3)

async def call_back(callback_query, state: FSMContext):
    cheak_ballans = get_balans_user(str(callback_query.message.chat.id))
    if cheak_ballans >= int(callback_query.message.text.split(" : ")[1]):
        await bot.send_message(callback_query.message.chat.id, f"Вы точно хотите потратить?", reply_markup=keyboard.kb_mark_4)
        async with state.proxy() as data:
            data["reason"] = callback_query.message.text.split(" : ")
    else:
        await bot.send_message(callback_query.message.chat.id, "Недостаточно средств", reply_markup=keyboard.kb_mark)
        await state.finish()

async def send_message_back(message, state: FSMContext):
    if str(message.from_user.id) in ID:
        await bot.send_message(message.from_user.id, "На главную", reply_markup=keyboard.kb_mark)
        await state.finish()

async def send_message_yes(message, state: FSMContext):
    if str(message.from_user.id) in ID:
        async with state.proxy() as data:
            make_purchase(acc_id=str(message.chat.id), reason=data['reason'][0], purchase_sum=-int(data['reason'][1]))
            await bot.send_message(message.from_user.id, f"Оплата прошла успешно", reply_markup=keyboard.kb_mark)
        await state.finish()


def register_handlers(dp):
    dp.register_message_handler(send_message_start, commands=["start"])
    dp.register_message_handler(send_message_balans, lambda message: "баланс" in message.text.lower() and str(message.from_user.id) in ID, state=None)
    dp.register_message_handler(send_message_get, lambda message: "как заработать" in message.text.lower() and str(message.from_user.id) in ID, state=None)
    dp.register_message_handler(send_message_buy_info, lambda message: "потратить" in message.text.lower() and str(message.from_user.id) in ID, state=None)
    dp.register_message_handler(send_message_back, lambda message: "на главную" in message.text.lower() and str(message.from_user.id) in ID, state=FSMAdmin.reason)
    dp.register_callback_query_handler(call_back, lambda callback: callback.data == "bt1", state=FSMAdmin.reason)
    dp.register_message_handler(send_message_yes, lambda message: "да" in message.text.lower() and str(message.from_user.id) in ID, state=FSMAdmin.reason)
