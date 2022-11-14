import time
import requests
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

# 用于终止函数
flag = False


def stop_update_watch_duration() -> None:
    global flag
    flag = True


def update_watch_duration(cookie: str, preview_id: str) -> None:
    '''用于每60s发送一次updateWatchDuration请求'''

    def get_data(preview_id) -> str:
        '''获取加密后的data'''
        public_key = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDoJCfMU6AG0Wc3zJqgVFhiPJVCFz0+3VCtjklx712todjRIX/d3CT4/t0xG07/YfZBuiXPr9kcBRahhEJNG8TcouDwLcZfBB+74kMy/EwWrErIUZvvuEmdOcxqGVeLJWr3rZb/I37rJkoz2pCFyQ3aYmIZ1xHTiqLWAkWc9iZC3wIDAQAB\n-----END PUBLIC KEY-----"

        # 每60s清零并发送updateWatchDuration请求，只有视频暂停时才停止计时
        message = '{"time":60,"previewId":"' + preview_id + '"}'
        key = public_key
        pub_key = RSA.importKey(str(key))
        cipher = PKCS1_cipher.new(pub_key)
        rsa_text = base64.b64encode(cipher.encrypt(bytes(message.encode("utf8"))))
        return rsa_text

    url = "https://stu.ityxb.com/back/bxg/preview/updateWatchDuration"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'text/plain',
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

    t = 0
    while True:
        if flag:
            break

        if t < 60:
            t += 1

        else:
            try:
                # RSA加密结果不确定，需要每次循环重新加密
                data = get_data(preview_id)
                res = requests.post(url, headers=headers, data=data).text
                # print("update_watch_duration", res)
                t = 0
            except Exception as e:
                print("发送updateWatchDuration请求失败", e)

        time.sleep(1)
