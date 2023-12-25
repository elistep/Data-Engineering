import os
import json
import msgpack
from pymongo import MongoClient

def load_data(file_name):
    with open(file_name, "rb") as f:
        byte_data = f.read()
    item = msgpack.unpackb(byte_data)
    return item

def insert_many(collection, data):
    result = collection.insert_many(data)
    #print(result)

def connect():
    client = MongoClient()
    db = client['test-database']
    return db.person

def first_query(collection):
    sort_bd = []
    for person in collection.find({}, limit=10).sort({'salary': -1}):
        person.pop('_id')
        sort_bd.append(person)
        #print(person)
    return sort_bd

bd_sort_salary = first_query(connect())
with open(("sort.json"), 'w', encoding='utf-8') as f:
    f.write(json.dumps(bd_sort_salary, ensure_ascii=False))

def second_query(collection):
    filter_db = []
    for person in collection.find({'age': {'$lt': 30}}, limit=15).sort({'salary': -1}):
        person.pop('_id')
        filter_db.append(person)
        # print(person)
    return filter_db

bd_filter_age = second_query(connect())
with open(("filter.json"), 'w', encoding='utf-8') as f:
    f.write(json.dumps(bd_filter_age, ensure_ascii=False))

def third_qyery(collection):
    filter_db = []
    for person in collection.find({'city': "Махадаонда",
                                   'job': {'$in': ["Психолог", "Продавец", 'Повар']}}, limit=10).sort({'age': 1}):
        person.pop('_id')
        filter_db.append(person)
        #print(person)
    return filter_db

bd_filter_city_job = third_qyery(connect())
with open(("city_job.json"), 'w', encoding='utf-8') as f:
    f.write(json.dumps(bd_filter_city_job, ensure_ascii=False))

def fourth_qyery(collection):
    filter_db = []
    res = collection.count_documents({'age': {"$gt": 30, "$lt": 50},
                                      'year': {"$in": [2019, 2020, 2021, 2022]},
                                      '$or': [{'salary': {"$gt": 50000, "$lte": 75000}},
                                              {'salary': {"$gt": 125000, "$lt": 150000}}]})
    filter_db.append({'count': res})
    return filter_db

count = fourth_qyery(connect())
with open(("count_filter.json"), 'w', encoding='utf-8') as f:
    f.write(json.dumps(count, ensure_ascii=False))

#
data = load_data("task_1_item.msgpack")
insert_many(connect(), data)
first_query(connect())
second_query(connect())
third_qyery(connect())
fourth_qyery(connect())