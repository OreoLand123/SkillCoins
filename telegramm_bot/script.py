import sys
sys.path.insert(0, "..")
from SkillCoins.functions import read_data, write_data, write_id
from datetime import datetime

def get_coins_info():
        reasons = read_data("Причины")
        json_dict = dict()
        for i in reasons:
            if i[0] == '':
                continue
            json_dict[i[0]] = i[1]
        return json_dict

def check_user_from(acc_id, acc_login):
    accounts = read_data("Аккаунты")
    accounts_id = []
    accounts_logins = []
    for i in accounts:
        try:
            accounts_logins.append(i[4])
        except IndexError:
            accounts_logins.append("0")
        accounts_id.append(i[1])
    if acc_id in accounts_id:
        return True
    else:
        if acc_login in accounts_logins:
            write_id(acc_id, acc_login, accounts_logins)
            return True
        else:
            return False

def check_user_id(acc_id, acc_login, ID):
    if acc_id in ID:
        return True
    if check_user_from(acc_id, acc_login):
        ID.append(acc_id)
        return True
    return False

def get_balance_user(acc_id):
    accounts = read_data("Аккаунты")
    for i in accounts:
        if acc_id == i[1]:
            if i[2] == "" or i[2] == "0":
                return 0
            else:
                return int(i[2])

def get_list_of_awards():
    reasons = read_data("Причины")
    json_dict = dict()
    for i in reasons:
        if i[0] == '':
            continue
        json_dict[i[3]] = int(i[4][1:])
    return json_dict

def make_purchase(acc_id, reason, purchase_sum):
    accounts = read_data("Аккаунты")
    past_logs = read_data("Логи")
    for acc in accounts:
        if acc_id == acc[1]:
            name = acc[0]
            break
    log = [[name, reason, purchase_sum, str(datetime.today()).split(".")[0]]]
    write_data("Логи", log, from_top=False)