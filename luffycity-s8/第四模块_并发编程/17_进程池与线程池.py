#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/1
# Location: DongGuang
# Desc:     do the right thing


from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from threading import currentThread
import time
import random
import os


def task(n):
    print(f'{currentThread().name} is running... PID:{os.getpid()}')
    time.sleep(random.randint(1, 5))
    return n ** 2


if __name__ == "__main__":
    executor_p = ProcessPoolExecutor(max_workers=3)   # 最多3个进程， 其它操作与ThreadPoolExecutor完全一致
    executor_t = ThreadPoolExecutor(max_workers=3)   # 最多3个线程

    futures_p = []
    for i in range(10):
        future_p = executor_p.submit(task, i)
        futures_p.append(future_p)
    executor_p.shutdown(True)   # 不再接受往池子里加任务
    print('>'.rjust(10, '>'))

    for future in futures_p:
        print(future.result())  # 获取任务结果

    futures_t = []
    for i in range(10):
        future_t = executor_t.submit(task, i)
        futures_t.append(future_t)
    executor_t.shutdown(True)   # 不再接受往池子里加任务
    print('>'.rjust(10, '>'))

    for future in futures_t:
        print(future.result())  # 获取任务结果

