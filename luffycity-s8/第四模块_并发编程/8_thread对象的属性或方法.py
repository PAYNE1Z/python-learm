#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/30
# Location: DongGuang
# Desc:     do the right thing


from threading import Thread, currentThread, enumerate, activeCount
import time


def task():
    # .name, .getName都是获取当前线程的名称（这里的当前线程就是t1,t2,t3了）
    print(f'{currentThread().getName()} running... ')
    time.sleep(1)
    print(f'{currentThread().name} done')


if __name__ == "__main__":
    t1 = Thread(target=task)
    t2 = Thread(target=task)
    t3 = Thread(target=task, name='Thread003')  # 初始化实例对象时，设定线程名称
    t_list = [t1, t2, t3]
    for t in t_list:
        t.start()

    t1.setName('起名好难')  # 设置t1线程名称
    print(t2.isAlive())  # 查看t2线程是否还活着，同is_alive()

    t3.join()  # 主线程等待t3线程结束

    # enumerate() 列表的方式返回当前进程下的所有正在运行线程对象
    # activeCount(), active_count() ：返回当前进程下正在运行线程的数量
    print(f'正在运行的线程: {enumerate()}, 共:{activeCount()}个')
    currentThread().setName('我是老大')     # 设置当前线程名称（这里当前线程就是主线程）
    print(f'主：{currentThread().name}')   # 主线和默认名称为 MainThread

    print(t3.isAlive())  # 前面t3.join()了 这里就是False了