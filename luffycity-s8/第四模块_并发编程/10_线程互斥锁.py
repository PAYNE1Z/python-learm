#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/30
# Location: DongGuang
# Desc:     do the right thing

import time
from threading import Thread, Lock


def change_variable(_lock):
    global n
    with _lock:  # 加锁 等同 _lock.acquire(), _lock.release()
        temp = n
        # 这里为了模拟所有线程同时来修改n变量，这里sleep一下，确保100个线程全部已起来
        # 不加sleep的话，因为线程是一个一个启的，而且很快，那么就会一个一个来修改这个值，很难造成数据错乱
        time.sleep(0.1)
        n = temp - 1


if __name__ == "__main__":
    n = 100
    t_list = []
    lock = Lock()
    for i in range(100):
        t = Thread(target=change_variable, args=(lock,))
        t_list.append(t)
        t.start()

    for t in t_list:
        t.join()

    print(f'main.. n: {n}')
    # main.. n: 99   加锁前
    # main.. n: 0    加锁后