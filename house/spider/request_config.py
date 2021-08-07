headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 "
                  "Safari/537.36",
    "sat": "730282",
    "sid": "20210428193417585",
    "code": "0",
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://www.sinyi.com.tw',
    'Referer': 'https://www.sinyi.com.tw/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}


def get_list_header(page=1, ret_range=None, ret_type=1):
    if ret_range is None:
        ret_range = ['1']

    return {
        "machineNo": "",
        "ipAddress": "203.218.155.48",
        "osType": 4,
        "model": "web",
        "deviceVersion": "Mac OS X 10.15.7",
        "appVersion": "92.0.4515.131",
        "deviceType": 3,
        "apType": 3,
        "browser": 1,
        "memberId": "",
        "domain": "www.sinyi.com.tw",
        "utmSource": "",
        "utmMedium": "",
        "utmCampaign": "",
        "utmCode": "",
        "requestor": 1,
        "utmContent": "",
        "utmTerm": "",
        "sinyiGroup": 1,
        "filter": {
            "exludeSameTrade": False,
            "objectStatus": 0,
            "retType": ret_type,
            "retRange": ret_range
        },
        "page": page,
        "pageCnt": 20,
        "sort": "0",
        "isReturnTotal": True
    }


def get_object_content_headers(house_no):
    return {
        "machineNo": "",
        "ipAddress": "203.218.155.48",
        "osType": 4,
        "model": "web",
        "deviceVersion": "Mac OS X 10.15.7",
        "appVersion": "92.0.4515.131",
        "deviceType": 3,
        "apType": 3,
        "browser": 1,
        "memberId": "",
        "domain": "www.sinyi.com.tw",
        "utmSource": "",
        "utmMedium": "",
        "utmCampaign": "",
        "utmCode": "",
        "requestor": 1,
        "utmContent": "",
        "utmTerm": "",
        "sinyiGroup": 1,
        "houseNo": house_no,
        "agentId": ""
    }


def get_object_detail_headers(house_no):
    return {
        "machineNo": "",
        "ipAddress": "203.218.155.48",
        "osType": 4,
        "model": "web",
        "deviceVersion": "Mac OS X 10.15.7",
        "appVersion": "92.0.4515.131",
        "deviceType": 3,
        "apType": 3,
        "browser": 1,
        "memberId": "",
        "domain": "www.sinyi.com.tw",
        "utmSource": "",
        "utmMedium": "",
        "utmCampaign": "",
        "utmCode": "",
        "requestor": 1,
        "utmContent": "",
        "utmTerm": "",
        "sinyiGroup": 1,
        "houseNo": house_no
    }
