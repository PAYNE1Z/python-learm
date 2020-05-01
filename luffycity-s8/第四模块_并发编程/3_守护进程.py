#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/29
# Location: DongGuang
# Desc:     do the right thing


from multiprocessing import Process
import time
import random
import os

# 如果我们有两个任务需要并发执行，那么开一个主进程和一个子进程分别去执行就ok了，
# 如果子进程的任务在主进程任务结束后就没有存在的必要了，那么该子进程应该在开启前就被设置成守护进程。
# 主进程代码运行结束，守护进程随即终止


def task(name):
    print(f'{name} is run... ppid: {os.getppid()}')
    time.sleep(random.randint(10))


if __name__ == "__main__":
    p = Process(target=task, args=('jack',))
    p.daemon = True  # 一定要在p.start()前设置,设置p为守护进程,禁止p创建子进程,并且父进程代码执行结束,p即终止运行
    p.start()

    print(f'主进程: {os.getpid()}')  # 只要终端打印出这一行内容，那么守护进程p也就跟着结束掉了


# 注意：主进程结束时，可能子进程根本还没有运行，但主进程已经结束，所有运行结果很大可能是看不到子进程输出内容的
