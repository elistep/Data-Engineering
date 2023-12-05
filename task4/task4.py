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

        root = BeautifulSoup(text, 'xml')

        for clothing in root.find_all("clothing"):
            item = dict()
            for el in clothing.contents:
                if el.name is None:
                    continue
                elif el.name == "price" or el.name == "reviews":
                    item[el.name] = int(el.get_text().strip())
                elif el.name == "price" or el.name == "rating":
                    item[el.name] = float(el.get_text().strip())
                elif el.name == "new":
                    item[el.name] = el.get_text().strip() == "+"
                elif el.name == "exclusive" or el.name == "sorty":
                    item[el.name] = el.get_text().strip() == "yes"
                else:
                    item[el.name] = el.get_text().strip()

            items.append(item)



    return items

items = []
for i in range(1, 100):
    file_name = f"zip_var_57.4/{i}.xml"
    result = handle_file(file_name)
    items += result

#сортируем по убыванию рейтинга
items = sorted(items, key=lambda x: x['rating'], reverse=True)

# записываем значения в json
with open("result_all_4.json", "w", encoding="utf-8") as f:
   f.write(json.dumps(items, ensure_ascii=False))

# фильтр без цвета Красный
filtered_items = []
for color in items:
     if color['color'] != 'Красный':
         filtered_items.append(color)

print(len(items))
print(len(filtered_items))

result = []

df = pd.DataFrame(items)
pd.set_option('display.float_format', '{:.1f}'.format)

stats = df['reviews'].agg(['max', 'min', 'mean', 'median', 'std']).to_dict()
result.append(stats)

#print(result)

result2 = []

material = [item['material'] for item in items]
f1 = collections.Counter(material)
result2.append(f1)

#print(result2)

#записываем отфильтрованные данные в json
with open("result_filtered_4.json", "w", encoding="utf-8") as f:
   f.write(json.dumps(filtered_items, ensure_ascii=False))

with open("math_4.json", "w", encoding="utf-8") as f:
   f.write(json.dumps(result, ensure_ascii=False))

with open("frequency_4.json", "w", encoding="utf-8") as f:
   f.write(json.dumps(result2, ensure_ascii=False))
