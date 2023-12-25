import json
import csv
from pymongo import MongoClient
from bson.json_util import dumps, loads

def connect():
    client = MongoClient()
    db = client['test-database']
    return db.person

def get_from_csv(filename):
    items = []
    with open(filename, 'r', encoding='utf-8') as f:
        data_csv = csv.reader(f, delimiter=';', quotechar='|')
        next(data_csv)
        for i in data_csv:
            # print(i)
            item = {
                'job': i[0],
                'salary': int(i[1]),
                'id': int(i[2]),
                'city': i[3],
                'year': int(i[4]),
                'age': int(i[5])
            }
            items.append(item)
    return items
def insert_many(collection, data):
    result = collection.insert_many(data)
    #print(result)

#вывод минимальной, средней, максимальной salary
def first_query(collection):
    q = [{
        "$group": {
            "_id":'result',
            "max":{"$max": "$salary"},
            "min":{"$min": "$salary"},
            "avg":{"$avg": "$salary"}
        }
    }]
    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
        json_data = dumps(result, indent = 2, ensure_ascii=False)
        with open(f'first.json', 'w', encoding='utf-8') as f:
            f.write(json_data)

# вывод количества данных по представленным профессиям
def second_query(collection):
    q = [{
        "$group": {
            "_id":'$job',
            "count":{"$sum": 1}
        }
    }, {
        "$sort": {
            "count":-1
        }
    }
    ]
    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    with open(f'second.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
# вывод минимальной, средней, максимальной salary по городу
def third_query(collection):
    q = [{
        "$group": {
            "_id":'$city',
            "max":{"$max": "$salary"},
            "min":{"$min": "$salary"},
            "avg":{"$avg": "$salary"}
        }
    }]
    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    with open(f'third.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
# вывод минимальной, средней, максимальной salary по профессии
def fourth_query(collection):
    q = [{
        "$group": {
            "_id":'$job',
            "max":{"$max": "$salary"},
            "min":{"$min": "$salary"},
            "avg":{"$avg": "$salary"}
        }
    }]
    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    with open(f'fourth.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
# вывод минимального, среднего, максимального возраста по городу
def fifth_query(collection):
    q = [{
        "$group": {
            "_id":'$city',
            "max":{"$max": "$age"},
            "min":{"$min": "$age"},
            "avg":{"$avg": "$age"}
        }
    }]
    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    with open(f'fifth.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
# вывод минимального, среднего, максимального возраста по профессии
def sixth_query(collection):
    q = [{
        "$group": {
            "_id":'$job',
            "max":{"$max": "$age"},
            "min":{"$min": "$age"},
            "avg":{"$avg": "$age"}
        }
    }]
    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    with open(f'sixth.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
# вывод максимальной заработной платы при минимальном возрасте
def seventh_query(collection):
    q = [
        {
            '$sort':{
                'age': 1,
                'salary': -1
            },
        },
        {'$limit': 10}
    ]

    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    with open(f'seventh.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
# вывод минимальной заработной платы при максимальной возрасте
def eight_query(collection):
    q = [
        {
            '$sort':{
                'age': -1,
                'salary': 1
            },
        },
        {'$limit': 10}
    ]
    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    with open(f'eight.json', 'w', encoding='utf-8') as f:
        f.write(json_data)

# вывод минимального, среднего, максимального возраста по городу, при условии,
# что заработная плата больше 50 000, отсортировать вывод по любому полю.
def ninth_query(collection):
    q = [{
            "$match": {
                "salary": {"$gt": 50_000}},
        },{
            "$group" : {
                "_id":'$city',
                "max":{"$max": "$age"},
                "min":{"$min": "$age"},
                "avg":{"$avg": "$age"}
            }
        }, {
            "$sort" : {
                "avg" : -1
            }
    }]
    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    with open(f'ninth.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
# вывод минимальной, средней, максимальной salary в произвольно заданных диапазонах по городу,
# профессии, и возрасту: 18<age<25 & 50<age<65
def tenth_query(collection):
    q = [{
            "$match": {
                "city": {"$in" : ['Санхенхо', 'Кишинев', 'Хельсинки']},
                "job": {"$in" : ['Медсестра', 'Учитель', 'Врач']},
                "$or": [
                    {'age': {"$gt":18, '$lt':25}},
                    {'age': {"$gt":50, '$lt':65}}
                ]
            }
        },{
            "$group" : {
                "_id":'result',
                "max":{"$max": "$salary"},
                "min":{"$min": "$salary"},
                "avg":{"$avg": "$salary"}
            }
        }]
    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    with open(f'tenth.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
# произвольный запрос с $match, $group, $sort
def eleventh_query(collection):
    q = [{
            "$match": {
                "city": {"$in": ['Гранада', 'Бургос', 'Артейхо']}
            }
        },{
            "$group" : {
                "_id":'result',
                "max":{"$max": "$salary"},
                "min":{"$min": "$salary"},
                "avg":{"$avg": "$salary"}
            }
        },
        {
            "$sort": {
                "min": -1
            }
        }]
    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    with open(f'eleventh.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
data = get_from_csv('task_2_item.csv')
insert_many(connect(), data)
first_query(connect())
second_query(connect())
third_query(connect())
fourth_query(connect())
fifth_query(connect())
sixth_query(connect())
seventh_query(connect())
eight_query(connect())
ninth_query(connect())
tenth_query(connect())
eleventh_query(connect())