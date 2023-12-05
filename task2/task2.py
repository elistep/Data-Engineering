from bs4 import BeautifulSoup
import re
import json
import math
import collections
import pandas as pd

def handle_file(file_name):
    items = list()
    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        products = site.find_all("div", attrs={'class': 'product-item'})

        for product in products:
            item = dict()
            item['id'] = product.a['data-id']
            item['link'] = product.find_all('a')[1]['href']
            item['img_url'] = product.find_all("img")[0]['src']
            item['title'] = product.find_all("span")[0].get_text().strip()
            item['price'] = int(product.price.get_text().replace("₽", "").replace(" ", "").strip())
            item['bonus'] = int(product.strong.get_text().replace("+ начислим ", "").replace(" бонусов", "").strip())

            props = product.ul.find_all("li")
            for prop in props:
                item[prop['type']] = prop.get_text().strip()

            items.append(item)
    return items

items = []
for i in range(1, 84):
    file_name = f"zip_var_57.2/{i}.html"
    items += handle_file(file_name)

#сортируем по убыванию цены
items = sorted(items, key=lambda x: x['price'], reverse=True)

# записываем значения в json
with open("result_all_2.json", "w", encoding="utf-8") as f:
   f.write(json.dumps(items, ensure_ascii=False))

#фильтр цена меньше 10050
filtered_items = []
for phone in items:
    if phone['price'] < 10050:
        filtered_items.append(phone)

#print(len(items))
#print(len(filtered_items))

result = []

df = pd.DataFrame(items)
pd.set_option('display.float_format', '{:.1f}'.format)

stats = df['price'].agg(['max', 'min', 'mean', 'median', 'std']).to_dict()
result.append(stats)

#print(result)

result2 = []

words = [item['title'] for item in items]
f1 = collections.Counter(words)
result2.append(f1)

#print(result2)

with open("result_filtered_2.json", "w", encoding="utf-8") as f:
   f.write(json.dumps(filtered_items, ensure_ascii=False))

with open("math_2.json", "w", encoding="utf-8") as f:
   f.write(json.dumps(result, ensure_ascii=False))

with open("frequency_2.json", "w", encoding="utf-8") as f:
   f.write(json.dumps(result2, ensure_ascii=False))
