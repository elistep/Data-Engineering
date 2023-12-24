import msgpack
import sqlite3
import json

def parce_data_mp(data_1):
    with open(data_1, 'rb') as mp_file:
        data_mp = msgpack.load(mp_file)
        for item in data_mp:
            item.pop('speechiness')
            item.pop('mode')
            item.pop('acousticness')
    return data_mp

def parce_data(data_2):
    items = []
    with open(data_2, 'r', encoding='utf-8') as file:
        data = file.readlines()
        item = dict()
        for i in data:
            if i == '=====\n':
                items.append(item)
                item = dict()
            else:
                i = i.strip()
                splitted = i.split('::')
                if splitted[0] == 'duration_ms' or splitted[0] == 'year':
                    item[splitted[0]] = int(splitted[1])
                elif splitted[0] == 'tempo':
                    item[splitted[0]] = float(splitted[1])
                elif splitted[0] == 'explicit' or splitted[0] == 'loudness':
                    continue
                else:
                    item[splitted[0]] = splitted[1]
    return items

# подключаемся к базе данных
def connect_to_db(elem):
    connection = sqlite3.connect(elem)
    connection.row_factory = sqlite3.Row
    return connection

def insert_price(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO music (artist, song, duration_ms, year, tempo, genre, instrumentalness)
        VALUES(
        :artist, :song, :duration_ms, :year, :tempo, :genre, :instrumentalness
        )
    """, data)
    db.commit()

def get_top_by_views(db, limit):
    cursor = db.cursor()
    result = cursor.execute("SELECT * FROM music ORDER BY artist DESC LIMIT ?", [limit])
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
            SUM(duration_ms) as sum,
            AVG(duration_ms) as avg,
            MIN(duration_ms) as min,
            MAX(duration_ms) as max
        FROM music
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
            artist as artist
            FROM music
            GROUP BY artist
        """)
    items = dict(result.fetchall())
    with open(f'frequency.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()
    return []
def get_sort_year(db,min_rating, limit):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT * 
        FROM music 
        WHERE year > ?
        ORDER BY year DESC 
        LIMIT ?
        """, [min_rating, limit])
    items = []
    for row in result.fetchall():
        items.append(dict(row))
    with open(f'filtered.json', 'w', encoding='utf-8') as file:
     file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()
    # return items
item_1 = parce_data_mp('task_3_var_57_part_1.msgpack')
item_2 = parce_data('task_3_var_57_part_2.text')
db = connect_to_db('first.db')
items = item_1 + item_2
#insert_price(db, items)
get_top_by_views(db, 67)
min_max(db)
get_occuerrence(db)
get_sort_year(db, 2010, 72)