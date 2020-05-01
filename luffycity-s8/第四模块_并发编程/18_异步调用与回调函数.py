#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/1
# Location: DongGuang
# Desc:     do the right thing


from concurrent.futures import ThreadPoolExecutor
from threading import currentThread
import time
import random
import requests


def get(_url):
    print(f'{currentThread().name} GET {_url}')
    response = requests.get(_url)
    time.sleep(random.randint(1, 3))
    if response.status_code == 200:
        return {'url': _url, 'text': response.text}

def parse(obj):
    data = obj.result()  # 回调函数要通过result()获取任务返回结果
    print(f'{currentThread().name} Parse: {data["url"]}  Size: {len(data["text"])}')


if __name__ == "__main__":
    executor = ThreadPoolExecutor(3)
    urls = [
        'https://www.baidu.com/',
        'https://www.taobao.com/',
        'https://www.sina.com/',
        'https://www.luffycity.com/',
        'https://www.163.com/'
    ]

    for url in urls:
        executor.submit(get, url).add_done_callback(parse)
        # parse拿到的是一个future对象obj，并将obj传递给parse函数，需要用obj.result()拿到结果