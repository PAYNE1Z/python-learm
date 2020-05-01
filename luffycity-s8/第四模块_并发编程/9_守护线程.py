#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/30
# Location: DongGuang
# Desc:     do the right thing


"""
无论是进程还是线程，都遵循：守护xxx会等待主xxx运行完毕后被销毁

主线程在其他非守护线程运行完毕后才算运行完毕（守护线程在此时就被回收）。
因为主线程的结束意味着进程的结束，进程整体的资源都将被回收，而进程必须保证非守护线程都运行完毕后才能结束。
"""

from threading import Thread
import time


# def sayhi(name):
#     time.sleep(2)
#     print(f'{name} say hello')
#
#
# if __name__ == '__main__':
#     t = Thread(target=sayhi, args=('egon',))
#     t.setDaemon(True)  # 必须在t.start()之前设置
#     t.start()
#
#     print('主线程')
#     print(t.is_alive())
#     # 除了t这个守护线程外没有别的线程要运行了，
#     # 所以当主线程运行到这里就结束了，此时t这个守护线程也随之终止，所以t线程运行的sayhi的语句不会被打印
#
#     # 结果：
#     # 主线程
#     # True


def foo():
    print('foo run')
    time.sleep(2)
    print('foo end')


def bar():
    print('bar run')
    time.sleep(3)
    print('bar end')


if __name__ == "__main__":
    t1 = Thread(target=foo)
    t2 = Thread(target=bar)

    t1.daemon = True   # 跟setDaemon(True)是一样的效果
    t1.start()
    t2.start()

    print('main...')
    # 当前进程中除了t1这个守护线程外，还有一个t2线程，
    # 所以主线程运行到这里还没算结束，要等t2运行结束，主线程也算结束，t1守护线程才跟着结束
    # t2运行中sleep了3秒，这时间t1中的内容也能全部输出

    # 结果:
    # foo run
    # bar run
    # main...
    # foo end
    # bar end