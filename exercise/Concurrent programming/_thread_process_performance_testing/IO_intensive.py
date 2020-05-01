#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/30
# Location: DongGuang
# Desc:     I/O 密集型程序在多进程与多线程情况下的性能测试


from multiprocessing import Process
from threading import Thread
import os
import time


def work():
    print('>>>', end='\r')


if __name__ == "__main__":
    total_job = 100
    print(f'LocalHostCPUs: {os.cpu_count()}')

    p_list, t_list = [], []
    p_st = time.time()
    for i in range(total_job):
        p = Process(target=work)
        p_list.append(p)
    for p in p_list:
        p.start()
    for p in p_list:
        p.join()
    p_et = time.time()
    print(f'{total_job} Process total run time: {p_et - p_st}')

    t_st = time.time()
    for i in range(total_job):
        t = Thread(target=work)
        t_list.append(t)
    for t in t_list:
        t.start()
    for t in t_list:
        t.join()
    t_et = time.time()
    print(f'{total_job} thread total run time: {t_et - t_st}')

    print(f'{total_job} performance gap [Process/Thread] : [{(p_et-p_st)/(t_et-t_st)}]')


# windows10:
# LocalHostCPU: 4
# 100 Process total run time: 7.193127393722534
# 100 thread total run time: 0.01303410530090332
# 100 performance gap [Process/Thread] : [521.7381203084134]
#
# LocalHostCPU: 4
# 10 Process total run time: 0.8642990589141846
# 10 thread total run time: 0.0010025501251220703
# 10 performance gap [Process/Thread] : [264.459793814433]

# Centos 7.3
# LocalHostCPUs: 16
# 100 Process total run time: 0.06836080551147461
# 100 thread total run time: 0.011934995651245117
# 100 performance gap [Process/Thread] : [5.727761241734753]
#
# LocalHostCPUs: 16
# 16 Process total run time: 0.014148950576782227
# 16 thread total run time: 0.002566099166870117
# 16 performance gap [Process/Thread] : [5.5137972684195855]


# 总结：
# 可以看到在纯I/O类型程序中，windows环境下，多线程性强于多进程上百倍，进程与线和数量越大，差距也越大
# linux环境下，多线程性强于多进程，进程与线和数量越大，差距也越大