#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/2
# Location: DongGuang
# Desc:     do the right thing

"""
对于单线程下，我们不可避免程序中出现io操作，
但如果我们能在自己的程序中（即用户程序级别，而非操作系统级别）控制单线程下的多个任务能在一个任务遇到io阻塞时就切换到另外一个任务去计算，
这样就保证了该线程能够最大限度地处于就绪态，即随时都可以被cpu执行的状态，
相当于我们在用户程序级别将自己的io操作最大限度地隐藏起来，
从而可以迷惑操作系统，让其看到：该线程好像是一直在计算，io比较少，从而更多的将cpu的执行权限分配给我们的线程。
"""

# 串行执行
import time


def consumer(_res):
    """任务1:接收数据,处理数据"""
    print(len(_res))


def producer():
    """任务2:生产数据"""
    _res = []
    for i in range(10000000):
        _res.append(i)
    return _res


start = time.time()
# 串行执行
res = producer()
consumer(res)         # 写成consumer(producer())会降低执行效率
stop = time.time()
print(stop - start)


# 基于yield并发执行

def consumer():
    """任务1:接收数据,处理数据"""
    while True:
        x = yield

def producer():
    """任务2:生产数据"""
    g = consumer()
    next(g)
    for i in range(10000000):
        g.send(i)


start = time.time()
# 基于yield保存状态,实现两个任务直接来回切换,即并发的效果
# PS:如果每个任务中都加上打印,那么明显地看到两个任务的打印是你一次我一次,即并发执行的.
producer()  # 并发执行,但是任务producer遇到io就会阻塞住,并不会切到该线程内的其他任务去执行
stop = time.time()
print(stop - start)
