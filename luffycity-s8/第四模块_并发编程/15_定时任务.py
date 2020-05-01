#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/1
# Location: DongGuang
# Desc:     定时器


from threading import Timer, currentThread


def work():
    print(f'{currentThread().name} Is work')


t = Timer(3, work)   # 3秒后执行work，开启新线程执行
print(f'{currentThread().name} With work start')
t.start()
t.join()
print(f'{currentThread().name} done')

# return
# MainThread With work start
# Thread-1 Is work
# MainThread done


