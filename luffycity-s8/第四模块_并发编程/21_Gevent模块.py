#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/2
# Location: DongGuang
# Desc:     do the right thing

"""
Gevent 是一个第三方库，可以轻松通过gevent实现并发同步或异步编程，在gevent中用到的主要模式是Greenlet,
它是以C扩展模块形式接入Python的轻量级协程。 Greenlet全部运行在主程序操作系统进程的内部，但它们被协作式地调度

#用法
g1=gevent.spawn(func,1,,2,3,x=4,y=5)创建一个协程对象g1，spawn括号内第一个参数是函数名，如eat，后面可以有多个参数，可以是位置实参或关键字实参，都是传给函数eat的
g2=gevent.spawn(func2)
g1.join() # 等待g1结束
g2.join() # 等待g2结束
# 或者上述两步合作一步：gevent.joinall([g1,g2])
g1.value  # 拿到func1的返回值
"""

import gevent
import time
from gevent import monkey;

monkey.patch_all()
from threading import currentThread


def eat(name):
    print(f'{name} eat 1')
    gevent.sleep(2)  # 模拟的gevent可以识别的io阻塞
    print(f'{name} eat 2')


def play(name):
    print(f'{name} play 1')
    gevent.sleep(1)
    print(f'{name} play 2')


g1 = gevent.spawn(eat, 'egon')
g2 = gevent.spawn(play, name='egon')
g1.join()
g2.join()
# 或者gevent.joinall([g1,g2])
print('主')


"""
上例gevent.sleep(2)模拟的是gevent可以识别的io阻塞,
而time.sleep(2)或其他的阻塞,gevent是不能直接识别的需要用下面一行代码,打补丁,就可以识别了
from gevent import monkey;monkey.patch_all()必须放到被打补丁者的前面，如time，socket模块之前
或者我们干脆记忆成：要用gevent，需要将from gevent import monkey;monkey.patch_all()放到文件的开头
"""

def eat():
    print(f'{currentThread().name} eat food 1')
    time.sleep(2)
    print(f'{currentThread().name} eat food 2')

def play():
    print(f'{currentThread().name} play 1')   # 可以看到线程名为 DummyThread-n , 即假线程
    time.sleep(1)
    print(f'{currentThread().name} play 2')


g1 = gevent.spawn(eat)
g2 = gevent.spawn(play)
gevent.joinall([g1, g2])
print('主')


# return
# egon eat 1
# egon play 1
# egon play 2
# egon eat 2
# 主

# DummyThread-1 eat food 1
# DummyThread-2 play 1
# DummyThread-2 play 2
# DummyThread-1 eat food 2
# 主