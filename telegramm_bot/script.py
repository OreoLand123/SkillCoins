
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'local-talent-364913-0febf38e0456.json')

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1oYSVwlNr2NZSB6i2pNHyKN0aW34Y50jldQgEKHUJiVw'
SAMPLE_RANGE_NAME = 'Причины'
SAMPLE_RANGE_NAME_ID = "Аккаунты"

service = build('sheets', 'v4', credentials=credentials)

sheet = service.spreadsheets()


def get_coins_info():
        reasons = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()["values"][2:]
        json_dict = dict()
        for i in reasons:
            if i[0] == '':
                continue
            json_dict[i[0]] = i[1]
        return json_dict


def buy_info():
    reasons = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()["values"][2:]
    json_dict = dict()
    for i in reasons:
        json_dict[i[3]] = i[4][1:]
    return json_dict


def cheak_user_from(acc_id, acc_login):
    accounts = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Аккаунты").execute()["values"][2:]
    accounts_id = []
    accounts_logins = []
    for i in accounts:
        try:
            accounts_logins.append(i[4])
        except IndexError:
            accounts_logins.append("0")
        accounts_id.append(i[1])
    if acc_id in accounts_id:
        return "1"
    else:
        if acc_login in accounts_logins:
            row_num = accounts_logins.index(acc_login) + 3
            results = service.spreadsheets().values().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"Аккаунты!B{row_num}",
                     "majorDimension": "ROWS",
                     "values": [[acc_id]]}
                ]
            }).execute()
            return "1"
        else:
            return "0"


def get_balans_user(acc_id):
    accounts = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Аккаунты").execute()["values"][2:]
    for i in accounts:
        if acc_id == i[1]:
            if i[2] == "" or i[2] == "0":
                return 0
            else:
                return int(i[2])


def sorted_list_of_awards():
    reasons = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()["values"][2:]
    json_dict = dict()
    for i in reasons:
        if i[0] == '':
            continue
        json_dict[i[3]] = int(i[4][1:])
    return json_dict


def make_purchase(acc_id, purchase_sum):
    accounts = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Аккаунты").execute()["values"][2:]
    reasons = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()["values"][2:]
    past_logs = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Логи").execute()["values"][2:]
    json_dict = {}
    for i in reasons:
        json_dict[i[3]] = i[4][1:]
    json_dict
    acc_id = "537932720"
    reason = "Получи 55% скидку на любой новый курс"
    for acc in accounts:
        if acc_id == acc[1]:
            name = acc[0]
            break
    log = [[name, reason, -json_dict[reason], str(datetime.today()).split(".")[0]]]

    logs = service.spreadsheets().values().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": f"Логи!A{len(past_logs) + 3}:D100",
            "majorDimension": "ROWS",    
            "values": log}
        ]
    }).execute()
    return log
