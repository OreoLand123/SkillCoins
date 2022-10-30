import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], ".."))
from functions import read_data, write_data, write_id
from datetime import datetime

async def get_coins_info():
    reasons = await read_data("Причины")
    json_dict = dict()
    for i in reasons:
        if i[0] == '':
            continue
        json_dict[i[0]] = i[1]
    return json_dict

async def check_user_from(acc_id, acc_login):
    accounts = await read_data("Аккаунты")
    accounts_id = []
    accounts_names = []
    accounts_logins = []
    for i in accounts:
        try:
            accounts_logins.append(i[4])
        except IndexError:
            accounts_logins.append("0")
        accounts_id.append(i[1])
        accounts_names.append(i[0])
    if acc_id in accounts_id:
        idx = accounts_id.index(acc_id)
        return accounts_names[idx]
    else:
        if acc_login in accounts_logins:
            await write_id(acc_id, acc_login, accounts_logins)
            idx = accounts_logins.index(acc_login)
            return accounts_names[idx]
        else:
            return None

async def check_user_id(acc_id, acc_login, ID):
    if acc_id in ID:
        return True
    user_name = await check_user_from(acc_id, acc_login)
    if user_name:
        ID[int(acc_id)] = user_name
        return True
    return False

async def get_balance_user(acc_id):
    accounts = await read_data("Аккаунты")
    for i in accounts:
        if acc_id == i[1]:
            if i[2] == "" or i[2] == "0":
                return 0
            else:
                return int(i[2])

async def get_list_of_awards():
    reasons = await read_data("Причины")
    json_dict = dict()
    for i in reasons:
        if i[0] == '':
            continue
        json_dict[i[3]] = int(i[4][1:])
    return json_dict

async def make_purchase(acc_id, reason, purchase_sum):
    accounts = await read_data("Аккаунты")
    past_logs = await read_data("Логи")
    for acc in accounts:
        if acc_id == acc[1]:
            name = acc[0]
            break
    log = [[name, reason, purchase_sum, str(datetime.today()).split(".")[0]]]
    await write_data("Логи", data=log, sheet_data=past_logs, from_top=False)

async def check_admin(acc_id, acc_log):
    admins = await read_data("Администраторы")
    id_list = [admin[1] for admin in admins]
    if acc_id in id_list:
        return True
    logins_list = [admin[2] for admin in admins]
    if acc_log in logins_list:
        await write_id(acc_id, acc_log, logins_list, sheet_name="Администраторы")
        return True
    return False
    