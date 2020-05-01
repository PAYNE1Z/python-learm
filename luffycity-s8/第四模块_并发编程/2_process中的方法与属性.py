#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/28
# Location: DongGuang
# Desc:     do the right thing


"""
在主进程运行过程中如果想并发地执行其他的任务，我们可以开启子进程，此时主进程的任务与子进程的任务分两种情况
情况一：在主进程的任务与子进程的任务彼此独立的情况下，主进程的任务先执行完毕后，主进程还需要等待子进程执行完毕，然后统一回收资源。
情况二：如果主进程的任务在执行到某一个阶段时，需要等待子进程执行完毕后才能继续执行，就需要有一种机制能够让主进程检测子进程是否运行完毕，
        在子进程执行完毕后才继续执行，否则一直在原地阻塞，这就是join方法的作用
"""

from multiprocessing import Process
import time
import random
import os


def task(name):
    print(f'{name} is running... ppid:{os.getppid()}')
    time.sleep(random.randrange(1, 5))


if __name__ == '__main__':
    p1 = Process(target=task, name='subprocess-1', args=('jack',))
    p2 = Process(target=task, args=('pony',))
    p3 = Process(target=task, args=('robin',))
    p_list = [p1, p2, p3]
    s_time = time.time()
    for p in p_list:
        p.start()
        print(f'子进程: {p.name}, pid: {p.pid}')
        # p.name 子进程的名称，可以在创建进程对象用name参数指定，默认为’Process-n‘
        # p.pid 子进程的pid

    for p in p_list:
        p.terminate()
        # 强制终止子进程，慎用！！！ ,
        # 关闭进程,不会立即关闭,跟start()一样只是给系统发了一个信号，什么时候杀还是由操作系统决定
        # 所以is_alive立刻查看的结果可能还是存活

    # 有的同学会有疑问: 既然join是等待进程结束, 那么我像下面这样写, 进程不就又变成串行的了吗?
    # 当然不是了, 必须明确：p.join()是让谁等？
    # 很明显p.join()是让主线程等待p的结束，卡住的是主进程而绝非子进程p，
    for p in p_list:
        p.join()  # 等待p停止,才执行下一行代码

    for p in p_list:
        p.is_alive()  # 查看子进程是否还活着

    # 进程只要start就会在开始运行了, 所以p1 - p3.start()
    # 时, 系统中已经有四个并发的进程了
    # 而我们p1.join()
    # 是在等p1结束, 没错p1只要不结束主线程就会一直卡在原地, 这也是问题的关键
    # join是让主线程等, 而p1 - p3仍然是并发执行的, p1.join的时候, 其余p2, p3, p4仍然在运行, 等
    # p1.join结束,可能p2,p3早已经结束了,这样p2.join,p3.join 直接通过检测，无需等待
    # 所以3个join花费的总时间仍然是耗费时间最长的那个进程运行的时间
    print('所有子进程已完成任务')
    print(f'主进程：pid: {os.getpid()}')
    print('run time:', time.time() - s_time)