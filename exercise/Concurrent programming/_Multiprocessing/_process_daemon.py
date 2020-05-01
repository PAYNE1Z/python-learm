#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/29
# Location: DongGuang
# Desc:     验证守护进程是在主进程结束后就结束


from multiprocessing import Process
import time


def foo():
    print(123)
    time.sleep(1)
    print("end123")


def bar():
    print(456)
    time.sleep(3)
    print("end456")


if __name__ == '__main__':
    p1 = Process(target=foo)
    p2 = Process(target=bar)

    p1.daemon = True
    p1.start()
    p2.start()
    print("main-------")


# return
# main-------
# 456
# end456

# 因为p1设置为了守护进程，主进程先结束了，所以没有p1进程的输出，
# 当然如果计算机性能非常强大，在p2.start() 或 主进程的print语句执行前就运行了p1,那么是能看到p1的输出的
# 但是只要主进程print语句执行完后，p1子进程也肯定结束了
