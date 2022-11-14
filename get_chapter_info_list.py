import time
import requests


def get_chapter_info_list(cookie: str, preview_id: str) -> list:
    '''获取所有未完成的视频信息'''

    time_stamp = str(int(time.time() * 1000))

    url = f"https://stu.ityxb.com/back/bxg/preview/info?previewId={preview_id}&t={time_stamp}"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": cookie,
        "dnt": "1",
        "referer": f"https://stu.ityxb.com/preview/detail/{preview_id}",
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
        all_chapter = res['resultObject']['chapters'][0]['points']

        chapter_info_list = []
        for chapter in all_chapter:
            # 判断任务是否已完成
            if chapter['progress100'] != 100:
                chapter_info = {
                    'name': chapter['point_name'],
                    'point_id': chapter['point_id'],
                    'video_duration': chapter['video_duration'],
                    'watched_duration': chapter['watched_duration'],
                }
                chapter_info_list.append(chapter_info)

        return chapter_info_list
    except Exception as e:
        print("获取章节信息失败", e)
        return []
