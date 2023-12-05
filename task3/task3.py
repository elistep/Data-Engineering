from bs4 import BeautifulSoup
import json
import pandas as pd
import collections
import re
import math

def handle_file(file_name):
    items = list()
    with open(file_name, encoding = "utf-8") as file:
        text = ""
        for row in file.readlines():
            text +=row

        star = BeautifulSoup(text, 'xml').star

        item = dict()
        for el in star.contents:
            if el.name == "radius":
                item[el.name] = int(el.get_text().strip())

            elif el.name is not None:
                item[el.name] = el.get_text().strip()

    return item

items = []
for i in range(1, 500):
    file_name = f"zip_var_57.3/{i}.xml"
    result = handle_file(file_name)
    items.append(result)

#сортируем по убыванию радиуса
items = sorted(items, key=lambda x: x['radius'], reverse=True)

# записываем значения в json
with open("result_all_3.json", "w", encoding="utf-8") as f:
   f.write(json.dumps(items, ensure_ascii=False))

#фильтр без знака Лев
filtered_items = []
for constellation in items:
    if constellation['constellation'] != 'Лев':
        filtered_items.append(constellation)

#print(len(items))
#print(len(filtered_items))

result = []

df = pd.DataFrame(items)
pd.set_option('display.float_format', '{:.1f}'.format)

stats = df['radius'].agg(['max', 'min', 'mean', 'median', 'std']).to_dict()
result.append(stats)

#print(result)

result2 = []

constellation = [item['constellation'] for item in items]
f1 = collections.Counter(constellation)
result2.append(f1)

#print(result2)

#записываем отфильтрованные данные в json
with open("result_filtered_3.json", "w", encoding="utf-8") as f:
   f.write(json.dumps(filtered_items, ensure_ascii=False))

with open("math.json", "w", encoding="utf-8") as f:
   f.write(json.dumps(result, ensure_ascii=False))

with open("frequency.json", "w", encoding="utf-8") as f:
   f.write(json.dumps(result2, ensure_ascii=False))


