import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'local-talent-364913-0febf38e0456.json')
SAMPLE_SPREADSHEET_ID = '1oYSVwlNr2NZSB6i2pNHyKN0aW34Y50jldQgEKHUJiVw'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()


def read_data(sheet_name):
    return sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=sheet_name).execute()["values"][2:]

def write_data(sheet_name, data, from_top=False, is_logs=True):
    res = read_data(sheet_name)
    start_row = 3 if from_top else 3 + len(res)
    start_col = "A" if is_logs else "D"
    service.spreadsheets().values().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"{sheet_name}!{start_col}{start_row}:D999",
                "majorDimension": "ROWS",    
                "values": data}
            ]
        }).execute()

def clear_logs():
    past_logs = read_data("Логи")
    f = [["", "", "", ""] for _ in past_logs]
    write_data("Логи", f, from_top=True, is_logs=True)