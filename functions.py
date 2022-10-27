import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath("functions.py"))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'local-talent-364913-0febf38e0456.json')
SAMPLE_SPREADSHEET_ID = '1oYSVwlNr2NZSB6i2pNHyKN0aW34Y50jldQgEKHUJiVw'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()


def read_data(sheet_name):
    return sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=sheet_name).execute()["values"][2:]

def write_data(sheet_name, data, sheet_data=None, from_top=False):
    if sheet_name == "История":
        sheet_data = read_data(sheet_name)
    start_row = 3 if from_top else 3 + len(sheet_data)
    if sheet_name == "Копия":
        start_col, finish_col = "C", "L"
    elif sheet_name == "Аккаунты":
        start_col, finish_col = "D", "D"
    elif sheet_name in ("История", "Логи"):
        start_col, finish_col = "A", "D"
    else:
        raise BaseException("Неизвестный лист")
    service.spreadsheets().values().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"{sheet_name}!{start_col}{start_row}:{finish_col}999",
                "majorDimension": "ROWS",    
                "values": data}
            ]
        }).execute()

def write_id(acc_id, acc_login, accounts_logins, sheet_name='Аккаунты'):
    row_num = accounts_logins.index(acc_login) + 3
    service.spreadsheets().values().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": f"{sheet_name}!B{row_num}",
            "majorDimension": "ROWS",
            "values": [[acc_id]]}
        ]
    }).execute()

def clear_logs(past_logs):
    f = [["", "", "", ""] for _ in past_logs]
    write_data("Логи", f, from_top=True)

def clear_rates(results):
    row_len = len(results[0][2:])
    minuses = [[" -"]*row_len for _ in results]
    write_data("Копия", minuses, from_top=True)
