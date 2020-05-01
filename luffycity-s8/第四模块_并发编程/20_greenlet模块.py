#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/2
# Location: DongGuang
# Desc:     do the right thing

"""
如果我们在单个线程内有20个任务，要想实现在多个任务之间切换，
使用yield生成器的方式过于麻烦（需要先得到初始化一次的生成器，然后再调用send。。。非常麻烦），
而使用greenlet模块可以非常简单地实现这20个任务直接的切换
"""

# 安装：pip3 install greenlet
from greenlet import greenlet


def eat(name):
    print(f'{name} eat 1')
    g2.switch('alex')   # 切换到play,并传参
    print(f'{name} eat 2')
    g2.switch('jack')         # 第二次不需要传参，即使传了，也没用（用的还是第一次传的值）

def play(name):
    print(f'{name} play 1')
    g1.switch()         # 切换到eat
    print(f'{name} play 2')


g1 = greenlet(eat)
g2 = greenlet(play)

g1.switch('egon')  # 可以在第一次switch时传入参数，以后都不需要

# return
# egon eat 1
# alex play 1
# egon eat 2
# alex play 2