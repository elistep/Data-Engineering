import json
import sqlite3

def parce_data(data):
    items = []
    with open(data, 'r', encoding='utf-8') as file:
        data_js = json.load(file)
        for i in data_js:
            items.append(i)
    return items

def connect_to_db(elem):
    connection = sqlite3.connect(elem)
    connection.row_factory = sqlite3.Row
    return connection

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO building (name, street, city, zipcode, floors, year, parking, prob_price, views)
        VALUES(
        :name, :street, :city, :zipcode, :floors, :year, :parking, :prob_price, :views
        )

    """, data)
    db.commit()

def get_top_by_views(db, limit):
    cursor = db.cursor()
    result = cursor.execute("SELECT * FROM building ORDER BY views DESC LIMIT ?", [limit])
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    with open(f'sorted.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()
    return items

def min_max(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT 
            SUM(views) as sum,
            AVG(views) as avg,
            MIN(views) as min,
            MAX(views) as max
        FROM building
        """)
    items = dict(result.fetchone())
    with open(f'math.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()
    return []

def get_occuerrence(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT 
            COUNT(*) as count,
            city as city
            FROM building
            GROUP BY city
        """)
    items = [dict(row) for row in result.fetchall()]
    with open(f'frequency.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()
    return []

def get_sort_year(db, min_year, limit):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT * 
        FROM building 
        WHERE year > ?
        ORDER BY year DESC 
        LIMIT ?
        """, [min_year, limit])
    items = []
    for row in result.fetchall():
        items.append(dict(row))
    with open(f'predicate.json', 'w', encoding='utf-8') as file:
     file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()
    return items

item = parce_data('task_1_var_57_item.json')
db = connect_to_db('first.db')
#insert_data(db, item)
get_top_by_views(db, 67)
min_max(db)
get_occuerrence(db)
get_sort_year(db, 1900, 67)