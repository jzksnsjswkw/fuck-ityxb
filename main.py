import threading
from get_course_dict import get_course_dict
from get_chapter_info_list import get_chapter_info_list
from update_progress import update_progress
from update_watch_duration import update_watch_duration, stop_update_watch_duration

# 手机号
phone = ''

# 自己抓
cookie = r''

# 课程id
course_id = ''

# 倍速，官网有 0.5 / 1 / 1.25 / 1.5 / 2 / 2.5
# 不怕封号拉满999
speed = 1


def fuck(cookie: str, speed: int, preview_id: str, chapter_info_list: list) -> None:
    '''刷某一章节的所有课'''

    update_watch_duration_thread = threading.Thread(
        target=update_watch_duration, args=(cookie, preview_id)
    )
    update_watch_duration_thread.start()

    for chapter_info in chapter_info_list:
        update_progress_thread = threading.Thread(
            target=update_progress, args=(cookie, speed, preview_id, chapter_info)
        )
        update_progress_thread.start()
        update_progress_thread.join()
        print()

    stop_update_watch_duration()
    update_watch_duration_thread.join()


course_dict = get_course_dict(cookie, phone, course_id)
for preview_id, course_name in course_dict.items():
    chapter_info_list = get_chapter_info_list(cookie, preview_id)
    print(course_name)
    fuck(cookie, speed, preview_id, chapter_info_list)
    print('-' * 50)
