import sqlite3
import json
from tabulate import tabulate

conn = sqlite3.connect('first.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS first
(id INTEGER, name TEXT, street TEXT, city TEXT, zipcode INTEGER, floors INTEGER, year INTEGER, 
parking TEXT, prob_price INTEGER, views INTEGER)''')


file_name = r'task_1_var_57_item.json'

with open(file_name, 'rb') as f:
    data = json.load(f)

for addres in data:
    id = addres['id']
    name = addres['name']
    street = addres['street']
    city = addres['city']
    zipcode = addres['zipcode']
    floors = addres['floors']
    year = addres['year']
    parking = addres['parking']
    prob_price = addres['prob_price']
    views = addres['views']

    cursor.execute("INSERT INTO first VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (id, name, street, city, zipcode, floors, year, parking, prob_price, views))

cursor.execute("SELECT * FROM first")
rows = cursor.fetchall()

headers = [description[0] for description in cursor.description]
print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

conn.commit()
conn.close()

conn = sqlite3.connect('first.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM first ORDER BY views ASC LIMIT 67")

data = []
for row in cursor.fetchall():
   data.append(dict(zip(headers, row)))
json_data = json.dumps(data, ensure_ascii=False, indent = 4)

with open('sorted.json', 'w', encoding='utf-8') as f:
   f.write(json_data)

conn.close()

conn = sqlite3.connect('first.db')
cursor = conn.cursor()

cursor.execute("SELECT SUM(prob_price), MIN(prob_price), MAX(prob_price), AVG(prob_price) FROM first")
result = cursor.fetchone()

print(f"Сумма: {result[0]}, Минимум: {result[1]}, Максимум: {result[2]}, Среднее: {result[3]}")

conn.close()

conn = sqlite3.connect('first.db')
cursor = conn.cursor()

print('Частота встречаемости:')
city_field = 'city'
cursor.execute(f"SELECT {city_field}, COUNT({city_field}) FROM first GROUP BY {city_field}")
results = cursor.fetchall()

for result in results:
   print(f"{result[0]}: {result[1]}")

conn.close()

conn = sqlite3.connect('first.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM first WHERE year > 1800")
cursor.execute("SELECT * FROM first WHERE year > 1800 ORDER BY year DESC")
cursor.execute("SELECT * FROM first WHERE year > 1800 ORDER BY year DESC LIMIT 67")

rows = cursor.fetchall()
headers = [description[0] for description in cursor.description]

data = []
for row in rows:
   data.append(dict(zip(headers, row)))

with open('filtered_predicate.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent = 4)

conn.close()