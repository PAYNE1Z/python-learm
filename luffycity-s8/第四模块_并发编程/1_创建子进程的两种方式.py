#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/28
# Location: DongGuang
# Desc:     do the right thing


from multiprocessing import Process
import time
import os


# 方式一, 直接使用Process类
def task(name):
    print(f'{os.getpid()}:{name} is start')
    time.sleep(3)
    print(f'{name} is end')


if __name__ == '__main__':
    p1 = Process(target=task, args=('jack',))    # target: 就是要交给子进程运行的任(函数), 给任务传递参数可用使用args 或 kwargs
    p2 = Process(target=task, kwargs={'name': 'pony'})
    p1.start()   # start就是给操作系统发了一个指令，主进程不会等待它执行，因为主进程管不到
    p2.start()

    print(f'{os.getpid()}: 这是主进程')   # 主进程的print会优先于子进程将执行


# 方式二, 自建一个Process类
class MyProcess(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self) -> None:
        print(f'{os.getpid()}:{self.name} is run')
        time.sleep(3)
        print(f'{self.name} is end')


if __name__ == '__main__':
    p3 = MyProcess('robin')
    p4 = MyProcess('alex')
    p3.start()
    p4.start()

    print(f'{os.getpid()}: 这是主进程')
