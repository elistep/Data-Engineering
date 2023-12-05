from bs4 import BeautifulSoup
import re
import json
import math
import collections
import pandas as pd

def handle_file(file_name):
    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')

        item = dict()
        item['genre'] = (site.find_all("span", string=re.compile("Категория:"))[0].get_text().split(":")[1].strip())
        item['title'] = site.find_all("h1")[0].get_text().strip()
        item['author'] = site.find_all("p")[0].get_text().strip()
        item['pages'] = int((site.find_all("span", attrs={'class': 'pages'})[0].get_text().split(":")[1].strip()).split(" ")[0].strip())
        item['year'] = int((site.find_all("span", attrs={'class': 'year'})[0].get_text().split("в")[1].strip()).split(" ")[0].strip())
        item['ISBN'] = (site.find_all("span", string=re.compile("ISBN:"))[0].get_text().split(":")[1].strip())
        item['description'] = site.find_all("p")[1].get_text().replace("Описание", "").strip()
        item['img_url'] = site.find_all("img")[0]['src']
        item['rating'] = float(site.find_all("span", string=re.compile("Рейтинг:"))[0].get_text().split(":")[1].strip())
        item['views'] = int(site.find_all("span", string=re.compile("Просмотры:"))[0].get_text().split(":")[1].strip())

        return item

handle_file("zip_var_57.1/2.html")

items = []
for i in range(1, 999):
    file_name = f"zip_var_57.1/{i}.html"
    result = handle_file(file_name)
    items.append(result)

#сортируем по убыванию кол-ва просмотров
items = sorted(items, key=lambda x: x['views'], reverse=True)

# записываем значения в json
with open("result_all_1.json", "w", encoding="utf-8") as f:
   f.write(json.dumps(items, ensure_ascii=False))

#фильтр без описания small
filtered_items = []
for book in items:
    if book['description'] != 'small':
        filtered_items.append(book)

print(len(items))
print(len(filtered_items))

result = []

df = pd.DataFrame(items)
pd.set_option('display.float_format', '{:.1f}'.format)

stats = df['pages'].agg(['max', 'min', 'mean', 'median', 'std']).to_dict()
result.append(stats)

print(result)

result2 = []

author = [item['author'] for item in items]
f1 = collections.Counter(author)
result2.append(f1)

print(result2)

with open("result_filtered_1.json", "w", encoding="utf-8") as f:
   f.write(json.dumps(filtered_items, ensure_ascii=False))

with open("math_1.json", "w", encoding="utf-8") as f:
       f.write(json.dumps(result, ensure_ascii=False))

with open("frequency_1.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(result2, ensure_ascii=False))


