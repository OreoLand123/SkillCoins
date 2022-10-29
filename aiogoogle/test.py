import api_client
import os

await api_client.InitializeClientAsync(os.path.join('..', 'resources', 'local-talent-364913-0febf38e0456.json'))
values = await api_client.GetClientAsync().GetValuesAsync(MASTER_SPREADSHEET_ID, ADMINS_RANGE_NAME)
print(values)