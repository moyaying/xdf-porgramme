import pymongo
from urllib.parse import quote_plus


def connect_db(db_name='house'):
    uri = "mongodb://%s:%s@%s" % (quote_plus('root'), quote_plus('password'), 'localhost:27017')
    client = pymongo.MongoClient(uri)
    return client[db_name]


def run_test():
    db = connect_db()
    collection = db.students

    print(db.list_collection_names())

    # student = {
    #     'id': '20170102',
    #     'name': '小明',
    #     'age': 21,
    #     'gender': '男性'
    # }
    #
    # result = collection.insert_one(student)
    # print(result)  # <pymongo.results.InsertOneResult object at 0x1034e08c8>
    # print(result.inserted_id)  # 5b1205b2d7696c4230dd9456


if __name__ == '__main__':
    run_test()
