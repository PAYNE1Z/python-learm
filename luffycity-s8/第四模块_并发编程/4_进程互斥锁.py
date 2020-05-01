#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/29
# Location: DongGuang
# Desc:     do the right thing


import os
import time
from multiprocessing import Process, Lock


def work(_lock):
    # _lock.acquire()  # 加锁
    # print(f'{os.getpid()} is running')
    # time.sleep(2)
    # print(f'{os.getpid()} is done')
    # _lock.release()  # 释放锁

    # 简化写法：
    with _lock:
        print(f'{os.getpid()} is running')
        time.sleep(2)
        print(f'{os.getpid()} is done')
    # 加锁就是确保哪个子进程先拿到锁就先执行完


if __name__ == '__main__':
    lock = Lock()
    for i in range(3):
        p = Process(target=work, args=(lock,))
        p.start()