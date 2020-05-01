#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/29
# Location: DongGuang
# Desc:     使用互诉锁模拟抢票


from multiprocessing import Process, Lock
import time
import json
import random


def load(json_file):
    with open(json_file, 'r', encoding='utf8') as f:
        data = json.load(f)
        return data


def search(name):
    time.sleep(random.random())  # 模拟网络延迟
    data = load('db.json')
    standby = data.get('count')
    if standby > 0:
        print(f'{name} 查询余票: {standby}')
    else:
        print(f'{name} 没票了...')


def get_ticket(name):
    time.sleep(random.random())  # 模拟网络延迟
    data = load('db.json')
    standby = data.get('count')
    if standby > 0:
        print(f'{name} 抢到车票')
        data['count'] -= 1
        with open('db.json', 'w') as fp:
            json.dump(data, fp)


def task(_lock, name):
    search(name)
    with _lock:  # 相当于lock.acquire(),执行完自代码块自动执行lock.release()
        get_ticket(name)


if __name__ == "__main__":
    ticket_data = {"count": 2}    # 车票原始数据数量
    with open('db.json', 'w', encoding='utf8') as f:
        json.dump(ticket_data, f)

    _lock = Lock()
    for i in range(10):
        p = Process(target=task, args=(_lock, f'<游客:{i}>'))
        p.start()


# join方法也能让并发变成串行，
# 但join会将整个task中的 search与get_ticket都变成串行
# 而lock是想让哪一个步骤变成串行，其它的仍然是并发执行的