#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/30
# Location: DongGuang
# Desc:     计算密集型程序在多进程与多线程情况下的性能测试


from multiprocessing import Process
from threading import Thread
import os
import time


def work(_count):
    ret = 1
    for n in range(1, _count):
        ret *= n


if __name__ == "__main__":
    total_job = 10
    count = 10000
    print(f'### Calculation 1-{count} product')
    print(f'LocalHostCPUs: {os.cpu_count()}')

    p_list, t_list = [], []
    p_st = time.time()
    for i in range(total_job):
        p = Process(target=work, args=(count,))
        p_list.append(p)
    for p in p_list:
        p.start()
    for p in p_list:
        p.join()
    p_et = time.time()
    print(f'{total_job} Process total run time: {p_et - p_st}')

    t_st = time.time()
    for i in range(total_job):
        t = Thread(target=work, args=(count,))
        t_list.append(t)
    for t in t_list:
        t.start()
    for t in t_list:
        t.join()
    t_et = time.time()
    print(f'{total_job} thread total run time: {t_et - t_st}')
    print(f'{total_job} performance gap [Thread/Process] : [{(t_et - t_st) / (p_et - p_st)}]')


# windows 10:
# ### Calculation 1-100000 product
# LocalHostCPUs: 4
# 10 Process total run time: 67.48748588562012
# 10 thread total run time: 109.961665391922
#
# ### Calculation 1-10000 product
# LocalHostCPUs: 4
# 10 Process total run time: 3.465813398361206
# 10 thread total run time: 1.1467676162719727


# Centos 7.3
# LocalHostCPUs: 16
# 100 Process total run time: 0.514000415802002
# 100 thread total run time: 5.650249719619751
# 100 performance gap [Thread/Process] : [10.992694842091884]
#
# LocalHostCPUs: 16
# 16 Process total run time: 0.13730716705322266
# 16 thread total run time: 0.9870908260345459
# 16 performance gap [Thread/Process] : [7.188924272626878]

# 总结：
# 可以看到在纯计算类型程序中，linux环境下多进程性强于多线程，进程与线和数量越大，差距也越大
# 在windows环境下 多进程要看计算机的性与计算公式的复杂度，
# 当计算复杂度高时，多进程性能会比多线程好
# 当计算复杂度低时，多线程依然比多进程好