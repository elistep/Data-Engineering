import json
import pickle
import msgpack
import csv
import os
import pandas as pd
import collections

crime = pd.read_csv('Crime_Data_from_2020_to_Present.csv', low_memory=False)
data = crime[['DR_NO', 'TIME OCC', 'Rpt Dist No', 'AREA NAME', 'Crm Cd Desc', 'Vict Age', 'Vict Sex']].head(None)
print(data)

result = list()
pd.set_option('display.float_format', '{:.2f}'.format)
result.append({
    'DR_NO_min' : int(crime['DR_NO'].min()),
    'DR_NO_max' : int(crime['DR_NO'].max()),
    'DR_NO_mean' : int(crime['DR_NO'].mean()),
    'DR_NO_std' : int(crime['DR_NO'].std()),
    'DR_NO_sum' : int(crime['DR_NO'].sum()),
    'TIME OCC_min': int(crime['TIME OCC'].min()),
    'TIME OCC_max': int(crime['TIME OCC'].max()),
    'TIME OCC_mean': int(crime['TIME OCC'].mean()),
    'TIME OCC_std': int(crime['TIME OCC'].std()),
    'TIME OCC_sum': int(crime['TIME OCC'].sum()),
    'Rpt Dist No_min' : int(crime['Rpt Dist No'].min()),
    'Rpt Dist No_max' : int(crime['Rpt Dist No'].max()),
    'Rpt Dist No_mean' : int(crime['Rpt Dist No'].mean()),
    'Rpt Dist No_std' : int(crime['Rpt Dist No'].std()),
    'Rpt Dist No_sum' : int(crime['Rpt Dist No'].sum()),
    'Vict Age_min' : int(crime['Vict Age'].min()),
    'Vict Age_max' : int(crime['Vict Age'].max()),
    'Vict Age_mean' : int(crime['Vict Age'].mean()),
    'Vict Age_std' : int(crime['Vict Age'].std()),
    'Vict Age_sum' : int(crime['Vict Age'].sum())
    })

crime1 = crime['AREA NAME']
f1 = collections.Counter(crime1)
result.append(f1)

crime2 = crime['Crm Cd Desc']
f2 = collections.Counter(crime2)
result.append(f2)

crime3 = crime['Vict Sex']
f3 = collections.Counter(crime3)
result.append(f3)

print(result)

# Сохраняем результат в json
with open("result.json", "w") as file:
    file.write(json.dumps(result))

with open("result.msgpack", "wb") as file:
    file.write(msgpack.dumps(result))

with open("result.pkl", "wb") as file:
    file.write(pickle.dumps(result))

print(f"json = {os.path.getsize('result.json')}")
print(f"msgpack = {os.path.getsize('result.msgpack')}")
print(f"pkl = {os.path.getsize('result.pkl')}")