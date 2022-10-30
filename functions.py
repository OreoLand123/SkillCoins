import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
import api_client
import os
import asyncio

MASTER_SPREADSHEET_ID = "1oYSVwlNr2NZSB6i2pNHyKN0aW34Y50jldQgEKHUJiVw"
BASE_DIR = os.path.dirname(os.path.abspath("__file__"))

async def fun():
    await api_client.InitializeClientAsync('local-talent-364913-0febf38e0456.json')
    return api_client

async def read_data(sheet_name):
    data = await api_client.GetClient().GetValuesAsync(MASTER_SPREADSHEET_ID, sheet_name)
    return data[2:]

async def write_data(sheet_name, data, sheet_data=None, from_top=False):
    start_row = 3 if from_top else 3 + len(sheet_data)
    if sheet_name == "Копия":
        start_col, finish_col = "C", "L"
    elif sheet_name == "Аккаунты":
        start_col, finish_col = "D", "D"
    elif sheet_name in ("История", "Логи"):
        start_col, finish_col = "A", "D"
    else:
        raise BaseException("Неизвестный лист")
    range = f"{sheet_name}!{start_col}{start_row}:{finish_col}999"
    await api_client.GetClient().AppendValuesAsync(id=MASTER_SPREADSHEET_ID, range=range, values=data)

async def write_id(acc_id, acc_login, accounts_logins, sheet_name='Аккаунты'):
    row_num = accounts_logins.index(acc_login) + 3
    range = f"{sheet_name}!B{row_num}"
    await api_client.GetClient().AppendValuesAsync(id=MASTER_SPREADSHEET_ID, range=range, values=[[acc_id]])

async def clear_logs(past_logs):
    f = [["", "", "", ""] for _ in past_logs]
    await write_data("Логи", f, from_top=True)

async def clear_rates(results):
    row_len = len(results[0][2:])
    minuses = [[" -"]*row_len for _ in results]
    await write_data("Копия", minuses, from_top=True)

loop = asyncio.get_event_loop()
api_client = loop.run_until_complete(fun())




