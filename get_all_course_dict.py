import requests


def get_all_course_dict(cookie: str, phone: str) -> dict:
    """获取课程字典

    Returns:
        dict: {'course_id': 'course_name'}
    """
    url = "https://stu.ityxb.com/back/bxg/course/getHaveList"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '32',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'dnt': '1',
        'login-name': phone,
        'origin': 'https://stu.ityxb.com',
        'referer': 'https://stu.ityxb.com/Classroom/course/learning',
        'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42',
    }

    data = {
        "type": "1",
        "pageNumber": "1",
        "pageSize": "100",
    }

    try:
        res = requests.post(url, headers=headers, data=data).json()
        buf = res['resultObject']['items']
        all_course_dict = {}
        for i in buf:
            all_course_dict[i['id']] = i['name']
        return all_course_dict

    except Exception as e:
        print("获取课程列表失败", e)
        return {}
