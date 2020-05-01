#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/28
# Location: DongGuang
# Desc:     练习


from multiprocessing import Process
import time
import random


# 效果一：保证最先输出-------->4
# -------->4
# -------->1
# -------->3
# -------->2

def task1(n):
    time.sleep(random.randint(1, 3))
    print(f'-------->{n}')


if __name__ == '__main__':
    p1 = Process(target=task1, args=(1,))
    p2 = Process(target=task1, args=(2,))
    p3 = Process(target=task1, args=(3,))
    s_time = time.time()
    p_list = [p1, p2, p3]
    for p in p_list:
        p.start()
    print(f'-------->4 run time: {time.time() - s_time}')   # 没有等等待子进程退出，所以这里的时间只是主进程运行的时间


# 效果二：保证最后输出-------->4
# -------->2
# -------->3
# -------->1
# -------->4

def task2(n):
    time.sleep(random.randint(1, 3))
    print(f'-------->{n}')


if __name__ == '__main__':
    p1 = Process(target=task2, args=(1,))
    p2 = Process(target=task2, args=(2,))
    p3 = Process(target=task2, args=(3,))
    s_time = time.time()
    p_list = [p1, p2, p3]
    for p in p_list:
        p.start()
    for p in p_list:
        p.join()
    print(f'-------->4 run time: {time.time() - s_time}')


# 效果三：保证按顺序输出
# -------->1
# -------->2
# -------->3
# -------->4

def task3(n):
    time.sleep(random.randint(1, 3))
    print(f'-------->{n}')


if __name__ == '__main__':
    p1 = Process(target=task3, args=(1,))
    p2 = Process(target=task3, args=(2,))
    p3 = Process(target=task3, args=(3,))
    s_time = time.time()
    p_list = [p1, p2, p3]
    for p in p_list:
        p.start()
        p.join()
    print(f'-------->4 run time: {time.time() - s_time}')


# 判断上述三种效果，哪种属于并发，哪种属于串行？
# 第一，第二种都是并发(程序总运行时长是运行时间最长的子进程的时间+主进程运行时间)，
# 第三种是串行(程序总运行时长是所有子进程与主进程的时间总合)
