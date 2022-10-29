import api_client
import os
import asyncio

MASTER_SPREADSHEET_ID = "1oYSVwlNr2NZSB6i2pNHyKN0aW34Y50jldQgEKHUJiVw"
BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
ADMINS_RANGE_NAME = "Логи"

async def fun():
    api_client.InitializeClient(os.path.join('local-talent-364913-0febf38e0456.json'))
    await api_client.InitializeClientAsync('local-talent-364913-0febf38e0456.json')
    # req = api_client.GetClientAsync()._spreadsheetAsync.values.batchUpdate(spreadsheetId=MASTER_SPREADSHEET_ID, json=ADMINS_RANGE_NAME)
    # await api_client.GetClientAsync()._aiogoogle.as_service_account(req)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fun())