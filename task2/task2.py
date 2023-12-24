import msgpack
import sqlite3
import json


def load_data(file_name):
    with open(file_name, "rb") as f:
        byte_data = f.read()
    data = msgpack.unpackb(byte_data)
    return data

#подключаемся к базе данных
def connect_to_db(elem):
    connection = sqlite3.connect(elem)
    connection.row_factory = sqlite3.Row
    return connection
def insert_info(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO comments (buildings_id, rating, convenience, security, functionality, comment)
        VALUES(
            (SELECT id FROM building WHERE name = :name),
            :rating, :convenience, :security, :functionality, :comment
        )
    """, data)
    db.commit()

def first_query(db, name):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT *
        FROM comments
        WHERE buildings_id = (SELECT id FROM building WHERE name = ?)
        """, [name])
    items = dict(result.fetchone())
    with open(f'first_query.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()
    return []

def second_query(db, name):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT
            AVG(security) as avg_security
        FROM comments
        WHERE buildings_id = (SELECT id FROM building WHERE name = ?)
        """, [name])
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    with open(f'second_query.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()

def third_query(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT
            name,
            (SELECT COUNT(*) FROM comments WHERE id = buildings_id) as city
        FROM building
        ORDER BY city
        LIMIT 10
        """)
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    with open(f'third_query.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()

item = load_data("task_2_var_57_subitem.msgpack")
db = connect_to_db('first.db')
insert_info(db, item)
first_query(db, 'Дупло 81')
second_query(db, 'Дупло 81')
third_query(db)