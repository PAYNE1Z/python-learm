#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/1
# Location: DongGuang
# Desc:     do the right thing


"""
线程的一个关键特性是每个线程都是独立运行且状态不可预测。
如果程序中的其 他线程需要通过判断某个线程的状态来确定自己下一步的操作,这时线程同步问题就会变得非常棘手。
为了解决这些问题,我们需要使用threading库中的Event对象。
对象包含一个可由线程设置的信号标志,它允许线程等待某些事件的发生。
在 初始情况下,Event对象中的信号标志被设置为假。如果有线程等待一个Event对象,
而这个Event对象的标志为假,那么这个线程将会被一直阻塞直至该标志为真。
一个线程如果将一个Event对象的信号标志设置为真,它将唤醒所有等待这个Event对象的线程。
如果一个线程等待一个已经被设置为真的Event对象,那么它将忽略这个事件, 继续执行


event.isSet()：返回event的状态值；
event.wait()：如果 event.isSet()==False将阻塞线程；
event.set()： 设置event的状态值为True，所有阻塞池的线程激活进入就绪状态， 等待操作系统调度；
event.clear()：恢复event的状态值为False。
"""


from threading import Thread, Event, currentThread
import time
import random

def conn_mysql():
    count = 1
    while not event.is_set():
        if count > 3:
            raise TimeoutError('链接超时')
        print(f'{currentThread().name}第{count}次尝试链接')
        event.wait(2)    # 等待event为True(check线程event.set()), (如果指定时间内还是False则继续往下执行)
        count += 1
    print(f'\033[1;36m{currentThread().name} 链接成功\033[0m')


def check_mysql():
    print(f'\033[1;34m[{currentThread().name}]正在检查MySQL连接\033[0m')
    time.sleep(random.randint(2, 4))
    event.set()  # 将event改为True(给conn_mysql线程)


if __name__ == '__main__':
    event = Event()
    conn1 = Thread(target=conn_mysql)
    conn2 = Thread(target=conn_mysql)
    check = Thread(target=check_mysql)

    conn1.start()
    conn2.start()
    check.start()


# return
# Thread-1第1次尝试链接
# Thread-2第1次尝试链接
# [Thread-3]正在检查MySQL连接
# Thread-1第2次尝试链接
# Thread-2第2次尝试链接
# Thread-2 链接成功
# Thread-1 链接成功