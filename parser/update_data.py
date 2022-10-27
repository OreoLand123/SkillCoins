import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], ".."))
from functions import read_data, write_data, clear_logs, clear_rates
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd

#---------------------READ DATA---------------------

results = read_data("Оценки")
reasons = read_data("Причины")
past_logs = read_data("Логи")
accounts_1 = read_data("Аккаунты")
accounts = [i[:4] for i in accounts_1]

#-------------------TRANSFORMATION-------------------

# Fill names on each row
j = ''
for i in results:
    if i[0] == '':
        i[0] = j
    j = i [0]


df = pd.DataFrame(results)
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

#-------------------CLOSE MONTH-------------------

try:
    if datetime.today().month != pd.to_datetime(past_logs_df.date[0]).month:
        amount_last_month = [[i[2]] for i in accounts]
        write_data("Аккаунты", data=amount_last_month, sheet_data=accounts_1, from_top=True)
        
        history = read_data("История")
        write_data('История', data=past_logs, from_top=False)

        clear_logs(past_logs)
        clear_rates(results)
except IndexError:
    pass

#-------------------INSERT DATA-------------------

if not logs_to_add.empty:
    l = [i.tolist() for i in logs_to_add.values]
    write_data("Логи", data=l, sheet_data=past_logs, from_top=False)