
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account



SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'local-talent-364913-14cc27db9b15.json')

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '10ToaB1UcUDcJtLCQdN2YNClWRL96XbN3MNuwJcVEVZw'
SAMPLE_RANGE_NAME = 'Main'


service = build('sheets', 'v4', credentials=credentials)

sheet = service.spreadsheets()
results = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
print(results)

