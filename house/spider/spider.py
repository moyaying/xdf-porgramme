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


def post_object_content(house_no):
    url = 'https://sinyiwebapi.sinyi.com.tw/getObjectContent.php'
    headers = request_config.headers
    payload = request_config.get_object_content_headers(house_no)
    response = requests.post(url=url, headers=headers, data=json.dumps(payload)).text
    response_json = json.loads(response)
    if response_json['retCode'] == '200':
        return response_json['content'], None
    else:
        return None, 'post_object_content error: house_no {0}, retCode {1}'.format(house_no, response_json['retCode'])


def post_object_detail(house_no):
    url = 'https://sinyiwebapi.sinyi.com.tw/getObjectDetail.php'
    headers = request_config.headers
    payload = request_config.get_object_detail_headers(house_no)
    response = requests.post(url=url, headers=headers, data=json.dumps(payload)).text
    response_json = json.loads(response)
    if response_json['retCode'] == '200':
        return response_json['content'], None
    else:
        return None, None, 'post_object_detail error: house_no {0}, retCode {1}'.format(house_no,
                                                                                        response_json['retCode'])


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


def start_crawl_list():
    pass


def start_crawl_content():
    # TODO
    pass


if __name__ == '__main__':
    # test_first_city_list()
    # test_object_content()
    # test_object_detail()
    test_crawl_insert_db('49340B')
