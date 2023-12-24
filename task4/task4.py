import msgpack
import sqlite3
import json

def parse_data(data_1):
   items = []
   with open(data_1, 'r', encoding='utf-8') as file:
       data_js = json.load(file)
       for i in data_js:
           i['category'] = i.get('category', 'no')
           items.append(i)
       return items

# подключаемся к базе данных
def connect_to_db(elem):
    connection = sqlite3.connect(elem)
    connection.row_factory = sqlite3.Row
    return connection
def insert_price(db, data):
    cursor = db.cursor()
    cursor.executemany("""
           INSERT INTO products (name, price, quantity, category, fromCity, isAvailable, views)
           VALUES(
           :name, :price, :quantity, :category, :fromCity, :isAvailable, :views
           )
       """, data)
    db.commit()
def delete_by_name(db, name):
    cursor = db.cursor()
    cursor.execute('DELETE FROM products WHERE name = ?', [name])
    db.commit()
def update_price_by_precent(db, name, precent):
    cursor = db.cursor()
    cursor.execute('UPDATE products SET price = ROUND((price * (1 + ?)), 2) WHERE name = ?', [precent, name])
    cursor.execute('UPDATE products SET version = version +1 WHERE  name = ?', [name])
    db.commit()
def quantity_add(db, name, quantity):
    cursor = db.cursor()
    res = cursor.execute('UPDATE products SET quantity = (quantity + ?) WHERE (name = ?) AND ((quantity + ?)> 0)', [quantity, name, quantity])
    if res.rowcount > 0:
        cursor.execute('UPDATE products SET version = version +1 WHERE  name = ?', [name])
        db.commit()
def price_abs(db, name, value):
    cursor = db.cursor()
    res = cursor.execute('UPDATE products SET price = (price + ?) WHERE (name = ?) AND ((price + ?)> 0)', [value, name, value])
    if res.rowcount > 0:
        cursor.execute('UPDATE products SET version = version +1 WHERE  name = ?', [name])
        db.commit()
def available(db, name, value):
    cursor = db.cursor()
    cursor.execute('UPDATE products SET isAvailable = ? WHERE (name = ?)', [value, name])
    cursor.execute('UPDATE products SET version = version +1 WHERE  name = ?', [name])
    db.commit()
def parse_data_mp(data_2):
    with open(data_2, 'rb') as mp_file:
        data_mp = msgpack.load(mp_file)
    for elem in data_mp:
        if elem['method'] == 'available' and elem['param'] == True:
            elem['param'] = 'True'
        elif elem['method'] == 'available' and elem['param'] == False:
            elem['param'] = 'False'
    return data_mp
def hungle_update(db, update_items):
    for item in update_items:
        match item['method']:
            case 'remove':
                print(f'Удалить {item["name"]}')
                delete_by_name(db, item["name"])
            case 'price_percent':
                print(f"Изменить на процент {item['name']} {item['param']}")
                update_price_by_precent(db, item['name'], item['param'])
            case 'price_abs':
                print(f"Изменение цены {item['name']} {item['param']}")
                price_abs(db, item['name'], item['param'])
            case 'available':
                print(f"Изменение доступности {item['name']} {item['param']}")
                available(db, item['name'], item['param'])
            case 'quantity_add':
                print(f"Изменение количества {item['name']} {item['param']}")
                quantity_add(db, item['name'], item['param'])
            case 'quantity_sub':
                print(f"Изменение количества {item['name']} {item['param']}")
                quantity_add(db, item['name'], item['param'])
#вывести топ-10 самых обновляемых товаров
def first_query(db, limit):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT *
        FROM products
        ORDER BY version DESC
        LIMIT ?
        """,[limit])
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    with open(f'top.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()

# проанализировать цены товаров, найдя (сумму, мин, макс, среднее) для каждой группы, а также количество товаров в группе
def min_max(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT
            SUM(price) as sum_price,
            AVG(price) as avg_price,
            MIN(price) as min_price,
            MAX(price) as max_price,
            SUM(quantity) as sum_quantity,
            AVG(quantity) as avg_quantity,
            MIN(quantity) as min_quantity,
            MAX(quantity) as max_quantity,
            SUM(views) as sum_views,
            AVG(views) as avg_views,
            MIN(views) as min_views,
            MAX(views) as max_views
        FROM products
        """)
    items = dict(result.fetchone())
    with open(f'math.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()
    return []
# проанализировать остатки товаров, найдя (сумму, мин, макс, среднее) для каждой группы товаров
def anasis_quality(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT category, AVG(quantity) as avg_price
        FROM products
        GROUP BY category
        """)
    items = dict(result.fetchall())
    with open(f'average.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()
    return []
# произвольный запрос
def second_query(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT
            COUNT(*) as count,
            fromCity as fromCity
            FROM products
            GROUP BY fromCity
        """)
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    with open(f'math2.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()
item_1 = parse_data('task_4_var_57_product_data.json')
db = connect_to_db('first.db')
insert_price(db, item_1)
item_2 = parse_data_mp('task_4_var_57_update_data.msgpack')
hungle_update(db, item_2)
first_query(db, 10)
min_max(db)
second_query(db)
anasis_quality(db)