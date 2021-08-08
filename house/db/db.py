import pymongo
from urllib.parse import quote_plus
from house.model import model


def connect_db(db_name='house'):
    uri = "mongodb://%s:%s@%s" % (quote_plus('root'), quote_plus('password'), 'localhost:27017')
    client = pymongo.MongoClient(uri)
    return client[db_name]


def run_insert_content(house_data):
    db = connect_db()
    collection = db.house
    # set index
    ensure_index(collection)

    result = collection.insert_one(house_data)
    print(house_data['houseNo'], result.inserted_id)


def save_last_position(city_id, page, total_cnt):
    db = connect_db()
    col = db.position
    record = col.find_one()
    position = {'city': city_id, 'page': page, 'total_cnt': total_cnt}
    if record is None:
        col.insert_one(position)
    else:
        position['_id'] = record['_id']
        col.replace_one({'_id': record['_id']}, position)


def get_last_position():
    db = connect_db()
    col = db.position
    record = col.find_one()
    if record is None:
        return {'city': 0, 'page': 0, 'total_cnt': 0}
    return record


def save_house_no_list(house_short_item):
    db = connect_db()
    col = db.house_index
    # set index
    col.ensure_index([("houseNo", 1)], unique=True)

    data = col.find_one({'houseNo': house_short_item['houseNo']})
    if data is None:
        result = col.insert_one(house_short_item)
        print(house_short_item['houseNo'], result.inserted_id)
    else:
        print(house_short_item['houseNo'], 'already exist')


def find_not_handle_house_index():
    db = connect_db()
    col = db.house_index
    return col.find({'handled': False}).limit(20)


def set_house_index_handled(house_no):
    db = connect_db()
    col = db.house_index
    col.find_one_and_update(
        {'houseNo': house_no},
        {'$set': {'handled': True}}
    )


def test_set_house_index_handled(house_no):
    set_house_index_handled(house_no)


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
    # h = run_query_by_house_no('04255Y1')
    # print(h)
    cursor = find_not_handle_house_index()
    print(cursor.count())
    for item in cursor:
        print(item)
    # test_set_house_index_handled('08357N')
    # save_last_position({'city': 2, 'page': 3})
    # pos = get_last_position()
    # print(pos)
