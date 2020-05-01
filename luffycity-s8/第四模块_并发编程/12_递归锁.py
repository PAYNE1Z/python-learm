#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/31
# Location: DongGuang
# Desc:     递归锁


"""
递归锁，用来解问解决死锁问题， 在Python中为了支持在同一线程中多次请求同一资源，python提供了可重入锁RLock。

这个RLock内部维护着一个Lock和一个counter变量，counter记录了acquire的次数，从而使得资源可以被多次require。
直到一个线程所有的acquire都被release，就是counter计算器为0时， 其他的线程才能获得资源。

互斥锁与递归锁二者的区别是：递归锁可以连续acquire多次，而互斥锁只能acquire一次
"""

# 递归锁
import time
from threading import Thread, RLock

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
    # lock_A = Lock()
    # lock_B = Lock()
    lock_A = lock_B = RLock()   # 将死锁示例中的两把锁改成同一RLock锁

    for i in range(1, 5):
        t = MyThread()
        t.start()


# 可以看到如下结果：
# Thread-1 get A lock, with B lock
# Thread-1 get B lock, release A and B lock
# Thread-1 get B lock, with A lock
# Thread-1 get A lock, release B and A lock
# Thread-2 get A lock, with B lock
# Thread-2 get B lock, release A and B lock
# Thread-2 get B lock, with A lock
# Thread-2 get A lock, release B and A lock
# Thread-4 get A lock, with B lock
# Thread-4 get B lock, release A and B lock
# Thread-4 get B lock, with A lock
# Thread-4 get A lock, release B and A lock
# Thread-3 get A lock, with B lock
# Thread-3 get B lock, release A and B lock
# Thread-3 get B lock, with A lock
# Thread-3 get A lock, release B and A lock

# RLock递归锁通过counter计算器让锁可以多次acquire, 直到counter为0，其它线程才能拿到锁，避免了死锁的出现