import json

import requests
from pymongo.errors import DuplicateKeyError

from house.spider import request_config
from house.model import model
from house.db import db


def post_list(page=1, city_range=None):
    url = 'https://sinyiwebapi.sinyi.com.tw/searchObject.php'
    headers = request_config.headers
    payload = request_config.get_list_header(page, city_range)
    response = requests.post(url=url, headers=headers, data=json.dumps(payload)).text
    response_json = json.loads(response)
    if response_json['retCode'] == '200':
        return response_json['content']['object'], response_json['content']['totalCnt'], None
    else:
        return None, 'post_list error: page {0}, city_range {1}, {2}'.format(page, city_range,
                                                                             response_json['retCode'])


def test_insert_house_list_index(page=1, city_range=None):
    houses, total_cnt, err = post_list(page, city_range)
    if err is not None:
        print(err)
        return

    print('found {0} items'.format(total_cnt))

    for house in houses:
        try:
            db.save_house_no_list({'houseNo': house['houseNo'], 'handled': False})
        except Exception as e:
            print(e)


def post_object_content(house_no):
    url = 'https://sinyiwebapi.sinyi.com.tw/getObjectContent.php'
    headers = request_config.headers
    payload = request_config.get_object_content_headers(house_no)
    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(payload)).text
        response_json = json.loads(response)
        if response_json['retCode'] == '200':
            return response_json['content'], None
        else:
            return None, 'post_object_content error: house_no {0}, retCode {1}'.format(house_no,
                                                                                       response_json['retCode'])
    except Exception as e:
        return None, str(e)


def post_object_detail(house_no):
    url = 'https://sinyiwebapi.sinyi.com.tw/getObjectDetail.php'
    headers = request_config.headers
    payload = request_config.get_object_detail_headers(house_no)
    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(payload)).text
        response_json = json.loads(response)
        if response_json['retCode'] == '200':
            return response_json['content'], None
        else:
            return None, None, 'post_object_detail error: house_no {0}, retCode {1}'.format(house_no,
                                                                                            response_json['retCode'])
    except Exception as e:
        return None, str(e)


def test_first_city_list():
    cities = list(model.all_city.keys())
    content, total, err = post_list(2, [cities[0]])
    if err is None:
        print(total)
        print(content)
    else:
        print(err)


def test_object_content():
    house_no = '04255Y'
    content, err = post_object_content(house_no)
    if err is None:
        print(content)
    else:
        print(err)


def test_object_detail():
    house_no = '04255Y'
    content, err = post_object_detail(house_no)
    if err is None:
        print(content)
    else:
        print(err)


def test_crawl_insert_db(house_no):
    content, err = post_object_content(house_no)
    if err is not None:
        print(err)
        return

    detail, err = post_object_detail(house_no)
    if err is not None:
        print(err)
        return

    m = merge_two_dicts(content, detail)
    try:
        db.save_content(m)
    except DuplicateKeyError as e:
        print(e)


def merge_two_dicts(x, y):
    """Given two dictionaries, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


def start_list():
    city_indexs = list(model.all_city.keys())

    # 上次进度
    last_position = db.get_last_position()
    for city_idx in city_indexs:
        print('start city {0}'.format(city_idx))
        if city_idx < last_position['city']:
            continue

        total_cnt = last_position['total_cnt']
        page = last_position['page']
        while page == 0 or total_cnt / 20 > page:
            page += 1
            print('拉取 city {0}, total_cnt {1}, page {2}'.format(city_idx, total_cnt, page))

            houses, total_cnt, err = post_list(page, [city_idx])
            if err is not None:
                print(err)
                continue

            print('入库 city {0}, total_cnt {1}, page {2}'.format(city_idx, total_cnt, page))
            for house in houses:
                try:
                    db.save_house_no_list({'houseNo': house['houseNo'], 'handled': False})
                except Exception as e:
                    print(e)

            print('保存进度 city {0}, total_cnt {1}, page {2}'.format(city_idx, total_cnt, page))
            db.save_last_position(city_idx, page, total_cnt)
            print('-------page end--------')
        last_position = {'city': city_idx, 'page': 0, 'total_cnt': 0}

    print('-------start list end--------')


def start_content():
    cursor = db.find_not_handle_house_index()
    while cursor.count() > 0:
        for item in cursor:
            house_no = item['houseNo']
            print('抓取 {0}'.format(house_no))
            content, err = post_object_content(house_no)
            if err is not None:
                print(err)
                continue

            detail, err = post_object_detail(house_no)
            if err is not None:
                print(err)
                continue

            m = merge_two_dicts(content, detail)
            print('入库 {0}'.format(house_no))
            try:
                db.save_content(m)
                db.set_house_index_handled(house_no)
            except Exception as e:
                print(e)

            print('--------end {0}----------'.format(house_no))

        print('开始新一批数据')
        cursor = db.find_not_handle_house_index()

    print('已全部爬取完毕')


if __name__ == '__main__':
    # test_first_city_list()
    # test_object_content()
    # test_object_detail()
    # test_crawl_insert_db('49340B')
    city = '1'
    test_insert_house_list_index(1, [city])
