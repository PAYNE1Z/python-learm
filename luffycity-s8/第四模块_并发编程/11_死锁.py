#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/31
# Location: DongGuang
# Desc:     do the right thing


"""
所谓死锁： 是指两个或两个以上的进程或线程在执行过程中，因争夺资源而造成的一种互相等待的现象，
若无外力作用，它们都将无法推进下去。此时称系统处于死锁状态或系统产生了死锁，这些永远在互相等待的进程称为死锁进程
"""

# 死锁示例
import time
from threading import Thread, Lock

class MyThread(Thread):  # 自定议Thread类
    def run(self):       # 一定要实现run方法
        self.func1()     # 执行func1, func2方法
        self.func2()

    def func1(self):
        lock_A.acquire()
        print(f'{self.name} get A lock, with B lock')

        lock_B.acquire()
        print(f'{self.name} get B lock, release A and B lock')

        lock_A.release()
        lock_B.release()

    def func2(self):
        lock_B.acquire()
        time.sleep(0.2)   # 因为线程开启足够快，而方法比较简单，执行很快，很难出现死锁象现，这里让func2慢一点
        print(f'{self.name} get B lock, with A lock')

        lock_A.acquire()
        print(f'{self.name} get A lock, release B and A lock')

        lock_B.release()
        lock_A.release()


if __name__ == '__main__':
    lock_A = Lock()
    lock_B = Lock()

    for i in range(1, 10):
        t = MyThread()
        t.start()


# 可以看到类似如下输出：
# Thread-1 get A lock, with B lock
# Thread-1 get B lock, release A and B lock
# Thread-2 get A lock, with B lock
# Thread-1 get B lock, with A lock

# 会有两个线程，其它一个拿到A锁，等B锁，而另一个线和拿到B锁，等A锁