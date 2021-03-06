#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/13
# Location: DongGuang
# Desc:     迭代器

"""
定义：
    凡是可作用于for循环的对象都是Iterable类型；
    凡是可作用于next()函数的对象都是Iterator类型，它们表示一个惰性计算的序列；
    集合数据类型如list、dict、str等是Iterable但不是Iterator，不过可以通过iter()函数获得一个Iterator对象。
"""

# Python3的for循环本质上就是通过不断调用next()函数实现的，例如：
for x in [1, 2, 3, 4, 5]:
    pass


# 实际上完全等价于：
it = iter([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])  # 首先获得Iterator对象:
while True:
    try:
        print(next(it))  # 获取下一个值
    except StopIteration as e:
        break
