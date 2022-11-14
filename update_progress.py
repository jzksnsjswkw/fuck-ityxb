from math import ceil
import time
import requests
from alive_progress import alive_bar
from get_poem import get_poem


def update_progress(
    cookie: str, speed: int, preview_id: str, chapter_info: dict
) -> None:
    '''更新视频进度'''

    name = chapter_info['name']
    point_id = chapter_info['point_id']
    # watchedDuration为当前视频已观看秒数，从上次观看秒数+1开始
    watched_duration = chapter_info['watched_duration'] + 1
    video_duration = chapter_info['video_duration']

    url = "https://stu.ityxb.com/back/bxg/preview/updateProgress"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '102',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'dnt': '1',
        'origin': 'https://stu.ityxb.com',
        'referer': f'https://stu.ityxb.com/preview/detail/{preview_id}',
        'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42',
    }

    data = {
        'previewId': preview_id,
        'pointId': point_id,
        'watchedDuration': watched_duration,
    }

    res = requests.post(url, headers=headers, data=data).text
    # print("update_progress开始", res)

    # 进度条
    number = ceil((video_duration - watched_duration) / (5 * speed))
    with alive_bar(len(range(number)), calibrate=5, title=name) as bar:
        for _ in range(number):
            bar()  # 显示进度
            bar.text(get_poem())

            # 刷完直接退出
            if watched_duration == video_duration:
                # print("update_progress结束")
                return

            try:
                # 时长足够时5s一次
                if video_duration - watched_duration >= 5 * speed:
                    time.sleep(5)
                    watched_duration += 5 * speed
                    data['watchedDuration'] = watched_duration
                    res = requests.post(url, headers=headers, data=data).text
                    # print("update_progress", res)

                # 时长不够，刷完最后一次结束
                else:
                    time.sleep((video_duration - watched_duration) / speed)
                    data['watchedDuration'] = video_duration
                    res = requests.post(url, headers=headers, data=data).text
                    # print("update_progress结束", res)
            except Exception as e:
                print("更新视频进度失败", e)
