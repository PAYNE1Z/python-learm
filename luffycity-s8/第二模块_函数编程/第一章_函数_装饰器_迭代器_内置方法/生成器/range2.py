#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/13
# Location: DongGuang
# Desc:     模拟range生成器


def range2(number):
    count = 0
    while count < number:
        print("before:", count)
        sign = yield count
        # 只有一个函数里面有yield，那么这个函数就是个生成器
        # yield 就是返回一个值并把程序暂停在这里，等待下次next调用
        # 并且可以接收send往生成器里面发的信息
        print("after:", count)
        if sign == 'stop':
            print('sign:', sign)
            break
        count += 1
    return 'Done'  # 在生成器中的return 信息会包含在Stopinteration报错信息里面


r = range2(3)
try:
    print(next(r), '\n----\n')  # 首次next会唤醒yield
    print(next(r), '\n----\n')
    r.send('stop')              # send会唤醒yield并往里面发送消息
    print(next(r), '\n----\n')
    print(next(r), '\n----\n')
except StopIteration as e:
    print("return value:", e.value)  # 在错误信息中获取return返回值