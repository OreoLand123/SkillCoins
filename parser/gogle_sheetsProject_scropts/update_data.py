import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath("scripts.py"))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'local-talent-364913-0febf38e0456.json')

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.

SAMPLE_SPREADSHEET_ID = '1oYSVwlNr2NZSB6i2pNHyKN0aW34Y50jldQgEKHUJiVw'
SAMPLE_RANGE_NAME = 'Оценки'
SAMPLE_RANGE_NAME_2 = 'Логи'


service = build('sheets', 'v4', credentials=credentials)

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()["values"][2:]
reasons = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Причины").execute()["values"][2:]
past_logs = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Логи").execute()["values"][2:]
accounts_1 = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Аккаунты").execute()["values"][2:]
accounts = [i[:4] for i in accounts_1]


# Fill names on each row

j = ''
for i in result:
    if i[0] == '':
        i[0] = j
    j = i [0]



df = pd.DataFrame(result)
df = df[df[1] != '']
df["sum_of_pluses"] = df[range(2,12)].T.apply(lambda x: x.str.count("\+")).sum()
df.drop(range(2,12), axis=1, inplace=True)
df.rename({0: 'student', 1: "reason"}, axis=1, inplace=True)


reasons_df = pd.DataFrame(reasons).drop([2, 3, 4], axis=1)
reasons_df.drop(reasons_df[reasons_df[1] == ""].index, inplace=True)


reasons_df.rename(columns={0: "reason", 1: "amount"}, inplace=True)
reasons_df.amount = reasons_df.amount.astype(int)


df = pd.merge(df, reasons_df)

df["to_add"] = df.sum_of_pluses * df["amount"].astype(int)

logs_df = pd.DataFrame(columns=['student', 'reason', 'amount', "date"])

from datetime import datetime
for row in df[df.sum_of_pluses != 0].values:
    for i in range(row[2]): 
        logs_df = logs_df.append({"student": row[0], "reason": row[1], "amount": row[3], "date": str(datetime.today()).split(".")[0]}, ignore_index=True)
logs_df.reset_index(drop=True, inplace=True)


if past_logs != []:
    past_logs_df = pd.DataFrame(past_logs)
    past_logs_df.rename(columns={0: 'student', 1: 'reason', 2: 'amount', 3: 'date'}, inplace=True)
    past_logs_df.amount = past_logs_df.amount.astype(int)
else:
    past_logs_df = pd.DataFrame(columns=['student', 'reason', 'amount', 'date'])


groups_past_logs = past_logs_df.groupby([past_logs_df.student, past_logs_df.reason, logs_df.amount], as_index=False).date.count()
groups_logs = logs_df.groupby([logs_df.student, logs_df.reason, logs_df.amount], as_index=False).date.count()
groups_logs = groups_logs.merge(groups_past_logs, on=['student', 'reason'], how="outer").fillna(0)
groups_logs["diff_count"] = groups_logs.date_x - groups_logs.date_y
logs_to_add = pd.DataFrame(columns=['student', 'reason', 'amount', 'date'])

for event in groups_logs[groups_logs.diff_count != 0].values:
    df = pd.DataFrame([[event[0], event[1], event[2], str(datetime.today()).split(".")[0]]], columns=['student', 'reason', 'amount', 'date'])
    for _ in range(int(event[-1])):
        logs_to_add = pd.concat([logs_to_add, df], ignore_index=True)

l = []
for i in logs_to_add.values:
    l.append(list(i))

start_row = len(past_logs) + 3

results_2 = service.spreadsheets().values().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body={
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": f"{SAMPLE_RANGE_NAME_2}!A{start_row}:D100",
         "majorDimension": "ROWS",    
         "values": l}
    ]
}).execute()

