import time
import requests


def get_course_dict(cookie: str, phone: str, course_id: str) -> dict:
    """获取某门课程 未完成且正在进行 的章节信息

    Returns:
        dict: {"preview_id": "preview_name"}
    """

    time_stamp = str(int(time.time() * 1000))
    url = f"https://stu.ityxb.com/back/bxg/preview/list?name=&isEnd=&pageNumber=1&pageSize=100&type=1&courseId={course_id}&t={time_stamp}"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": cookie,
        "dnt": "1",
        "login-name": phone,
        "referer": f"https://stu.ityxb.com/learning/{course_id}/preview/list",
        "sec-ch-ua": '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42",
    }

    try:
        res = requests.get(url, headers=headers).json()

        # 官网默认新章节在前
        buf = res['resultObject']['items'][::-1]
        course_dict = {}
        for i in buf:
            if i['statusText'] == '未完成' and i['endStatusText'] == '进行中':
                course_dict[i['id']] = i['preview_name']
        return course_dict

    except Exception as e:
        print("获取课程失败", e)
        return {}
