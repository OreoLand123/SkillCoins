from create_bot import bot
import keyboard_tg
from script import get_coins_info, get_balance_user, get_list_of_awards, make_purchase, check_user_id, check_admin
from States import FSMAdmin, FSMContext
from text import texts
import random
from parser.update_data import main


ID = {}
admin_ID = None
admin_login = None


async def send_message_start(message):
    global admin_ID
    global admin_login
    if await check_admin(str(message.from_user.id), message.from_user.username):
        admin_ID = message.from_user.id
        admin_login = message.from_user.username
        await bot.send_message(message.from_user.id, texts["hello_admin"], reply_markup=keyboard_tg.kb_mark_6)
    elif not await check_user_id(str(message.from_user.id), message.from_user.username, ID):
        await bot.send_message(message.from_user.id, random.choice(texts["dont_bd_user"]).format(admin_login), reply_markup=keyboard_tg.kb_mark_5)
    else:
        await bot.send_message(message.from_user.id, random.choice(texts["hello"]).format(ID[message.from_user.id].split(' ')[1]), reply_markup=keyboard_tg.kb_mark)

async def send_message_balance(message):
    if await check_user_id(str(message.from_user.id), message.from_user.username, ID):
        balance = await get_balance_user(str(message.from_user.id))
        mes = texts["balance_0"] if balance == 0 else texts["balance"]
        await bot.send_message(message.from_user.id, random.choice(mes).format(balance), reply_markup=keyboard_tg.kb_mark)
    else:
        await bot.send_message(message.from_user.id, random.choice(texts["dont_bd_user"]).format(admin_login))

async def send_message_get(message):
    if await check_user_id(str(message.from_user.id), message.from_user.username, ID):
        get_coins = await get_coins_info()
        text = ""
        for i in get_coins:
            text += i + " : " + get_coins[i] + "\n\n"
        await bot.send_message(message.from_user.id, f"💫 Как ты можешь заработать 💫: \n\n{text}", reply_markup=keyboard_tg.kb_mark)
    else:
        await bot.send_message(message.from_user.id, random.choice(texts["dont_bd_user"]).format(admin_login))

async def send_message_buy_info(message):
    if await check_user_id(str(message.from_user.id), message.from_user.username, ID):
        list_of_awards = await get_list_of_awards()
        await FSMAdmin.reason.set()
        await bot.send_message(message.from_user.id, random.choice(texts["buy_info"]), reply_markup=keyboard_tg.kb_mark_2)
        for i in list_of_awards:
            await bot.send_message(message.from_user.id, f"{i} : {list_of_awards[i]}", reply_markup=keyboard_tg.kb_mark_3)
    else:
        await bot.send_message(message.from_user.id, random.choice(texts["dont_bd_user"]).format(admin_login))

async def call_back(callback_query, state: FSMContext):
    cheak_ballans = await get_balance_user(str(callback_query.message.chat.id))
    if cheak_ballans >= int(callback_query.message.text.split(" : ")[1]):
        await bot.send_message(callback_query.message.chat.id, f"Вы точно хотите потратить?", reply_markup=keyboard_tg.kb_mark_4)
        async with state.proxy() as data:
            data["reason"] = callback_query.message.text.split(" : ")
    else:
        await bot.send_message(callback_query.message.chat.id, random.choice(texts["dont_coins"]), reply_markup=keyboard_tg.kb_mark)
        await state.finish()

async def send_message_back(message, state: FSMContext):
    if await check_user_id(str(message.from_user.id), message.from_user.username, ID):
        await bot.send_message(message.from_user.id, "Выбери одно из предложенных действий👇🏻", reply_markup=keyboard_tg.kb_mark)
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, random.choice(texts["dont_bd_user"]).format(admin_login))

async def send_message_yes(message, state: FSMContext):
    if await check_user_id(str(message.from_user.id), message.from_user.username, ID):
        async with state.proxy() as data:
            await make_purchase(acc_id=str(message.chat.id), reason=data['reason'][0], purchase_sum=-int(data['reason'][1]))
            await bot.send_message(message.from_user.id, f"Оплата прошла успешно", reply_markup=keyboard_tg.kb_mark)
            await state.finish()
        if admin_ID != None and admin_login != None:
            await bot.send_message(admin_ID, random.choice(texts["message_admin"]).format(f"{ID[message.chat.id]} потратил(а) на {data['reason'][0]} {int(data['reason'][1])} SkillCoins"))
            await state.finish()
    else:
        await bot.send_message(message.from_user.id, random.choice(texts["dont_bd_user"]).format(admin_login))

async def send_message_update(message):
    if await check_admin(str(message.from_user.id), message.from_user.username):
        res = await main()
        mes = texts["update_logs_0"] if res[0] == 0 else texts["update_logs"]
        await bot.send_message(message.from_user.id, random.choice(mes).format(str(res[0])), reply_markup=keyboard_tg.kb_mark_6)
        if res[1] != []:
            errors_mes = ''
            for err in res[1]:
                errors_mes += f"{err[2]} лишних логов: {err[0]} {err[1]}\n"
            await bot.send_message(message.from_user.id, random.choice(texts["errors"]).format(errors_mes), reply_markup=keyboard_tg.kb_mark_6)

def register_handlers(dp):
    dp.register_message_handler(send_message_start, commands=["start"])
    dp.register_message_handler(send_message_balance, lambda message: "баланс" in message.text.lower(), state=None)
    dp.register_message_handler(send_message_get, lambda message: "как заработать" in message.text.lower(), state=None)
    dp.register_message_handler(send_message_buy_info, lambda message: "потратить" in message.text.lower(), state=None)
    dp.register_message_handler(send_message_back, lambda message: "на главную" in message.text.lower(), state=FSMAdmin.reason)
    dp.register_callback_query_handler(call_back, lambda callback: callback.data == "bt1", state=FSMAdmin.reason)
    dp.register_message_handler(send_message_yes, lambda message: "да" in message.text.lower(), state=FSMAdmin.reason)
    dp.register_message_handler(send_message_update, lambda message: "обновить логи" in message.text.lower(), state=None)
