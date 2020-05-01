#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/30
# Location: DongGuang
# Desc:     do the right thing

# 同一进程内的线程共享该进程的数据？

from threading import Thread, currentThread, current_thread


def work():
    global n
    print(f'{currentThread().name}修改前: {n}')
    n = 0
    print(f'{current_thread().name}修改后: {n}')
    # current_thread currentThread 两个方法都是获取当前运行线程的名称


if __name__ == "__main__":
    n = 100
    t1 = Thread(target=work)
    t2 = Thread(target=work)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print(f'主: {n}')

# 可以看到结果，当线程t1运行时n=100,之后改成了0， t2线程运行时n已经是0了，最后主线程输出时也是0
# 这也就验证是同一进程下多个线程间的数据是共享的
# Thread-1修改前: 100
# Thread-1修改后: 0
# Thread-2修改前: 0
# Thread-2修改后: 0
# 主: 0