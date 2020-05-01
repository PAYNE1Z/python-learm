#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/31
# Location: DongGuang
# Desc:     do the right thing

"""
信号量也是一把锁，可以指定信号量为5，
对比互斥锁同一时间只能有一个任务抢到锁去执行，信号量同一时间可以有5个任务拿到锁去执行
"""
import time
from threading import Thread, Semaphore, currentThread, activeCount

sm = Semaphore(3)  # 信号量锁对象（允许同时三个线程拿到锁)

def task():
    with sm:  # sm.acquire; sm.release
        print(f'{currentThread().name} is work...')
        print(f'activeCount: {activeCount()}')
        time.sleep(3)
        print(f'{currentThread().name} is done...')


if __name__ == "__main__":
    for i in range(10):
        t = Thread(target=task)
        t.start()

