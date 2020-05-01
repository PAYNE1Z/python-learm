#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/28
# Location: DongGuang
# Desc:     验证进程之间内存是隔离的


from multiprocessing import Process


def work():
    global n
    n = 0
    print(f'子进程内: {n}')


n = 100  # 在windows系统中应该把全局变量定义在if __name__ == '__main__'之上就可以了
if __name__ == '__main__':
    p = Process(target=work)
    p.start()
    p.join()
    print(f'主进程内: {n}')

# 不管子进程怎么改，主进程所引用的全局变量的值不会被修改
# 子进程内: 0
# 主进程内: 100
