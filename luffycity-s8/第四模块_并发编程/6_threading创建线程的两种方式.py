#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/30
# Location: DongGuang
# Desc:     do the right thing


from threading import Thread
import os
import time

# 方式一、


def task(name):
    print(f'{name} is running... PID:{os.getpid()}, PPID:{os.getppid()}')
    time.sleep(60)
    print(f'{name} is done...')


if __name__ == "__main__":
    t = Thread(target=task, args=('jack',))
    t.start()   # 创建线程，不需要申请内存空间，相比于创建进程，要快得多，所以很大机率 t线程中的第一条输出会比主线程的输出要早

    print(f'主, PID:{os.getpid()}')


# 方式二、 自建线程类


class MyThread(Thread):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print(f'{self.name} is running... PID:{os.getpid()}, PPID:{os.getppid()}')
        time.sleep(60)
        print(f'{self.name} is done...')


if __name__ == "__main__":
    t = MyThread('pony')
    t.start()

    print(f'主, PID:{os.getpid()}')


# 1、线程没有主线程和子线程之分， 主线程其实是叫控制线程
# 2、所有线程都是一个进程内的，所有它们的pid都是一样的，在本例中，pid就是python解释器的进程pid, ppid就是pycharm的pid