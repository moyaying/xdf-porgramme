import pymongo
from urllib.parse import quote_plus
from house.model import model


def connect_db(db_name='house'):
    uri = "mongodb://%s:%s@%s" % (quote_plus('root'), quote_plus('password'), 'localhost:27017')
    client = pymongo.MongoClient(uri)
    return client[db_name]


def run_insert(house_data):
    db = connect_db()
    collection = db.house
    # set index
    ensure_index(collection)

    result = collection.insert_one(house_data)
    print(house_data['houseNo'], result.inserted_id)


def save_content(house_data):
    db = connect_db()
    collection = db.house
    # set index
    ensure_index(collection)

    data = collection.find_one({'houseNo': house_data['houseNo']})
    if data is None:
        result = collection.insert_one(house_data)
        print(house_data['houseNo'], result.inserted_id)
    else:
        collection.update_one(
            {'houseNo': house_data['houseNo']},
            {'$set': house_data}
        )
        print('update {0}'.format(house_data['houseNo']))


def ensure_index(col):
    # set index
    col.ensure_index([("houseNo", 1)], unique=True)
    col.ensure_index([("cityId", 1)])


def run_query_by_house_no(house_no):
    db = connect_db()
    collection = db.house
    return collection.find_one({"houseNo": house_no})


if __name__ == '__main__':
    h = run_query_by_house_no('04255Y1')
    print(h)
