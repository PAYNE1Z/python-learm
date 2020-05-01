#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/2
# Location: DongGuang
# Desc:     do the right thing


"""
同一线程下，任务串行，与切换执行，效率对比测试
"""
import time
from greenlet import greenlet


# 1、顺序执行
def f1():
    res = 1
    for i in range(100000000):
        res += i

def f2():
    res = 1
    for i in range(100000000):
        res *= i


start = time.time()
f1()
f2()
stop = time.time()
print('Serial run time is %s' % (stop - start))


# 2、切换执行
def f1():
    res = 1
    for i in range(100000000):
        res += i
        g2.switch()

def f2():
    res = 1
    for i in range(100000000):
        res *= i
        g1.switch()


start = time.time()
g1 = greenlet(f1)
g2 = greenlet(f2)
g1.switch()
stop = time.time()
print('Switch run time is %s' % (stop - start))


# return
# Serial run time is 9.510720252990723
# Switch run time is 56.61751389503479

# 结论：
# 单纯的切换（在没有io的情况下或者没有重复开辟内存空间的操作），反而会降低程序的执行速度