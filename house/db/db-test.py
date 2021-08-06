import pymongo
from urllib.parse import quote_plus


def run_test():
    uri = "mongodb://%s:%s@%s" % (
        quote_plus('root'), quote_plus('password'), 'localhost:27017')
    client = pymongo.MongoClient(uri)
    print(client.list_database_names())

    db = client.mydb
    collection = db.students

    student = {
        'id': '20170101',
        'name': '小明',
        'age': 22,
        'gender': '男性'
    }

    result = collection.insert_one(student)
    print(result)  # <pymongo.results.InsertOneResult object at 0x1034e08c8>
    print(result.inserted_id)  # 5b1205b2d7696c4230dd9456


if __name__ == '__main__':
    run_test()
