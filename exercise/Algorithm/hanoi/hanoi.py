#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/10/30
# Location: DongGuang
# Desc:     递归实现汉诺塔

x = 0
def hanoi(n, a, b, c):
    global x
    if n > 0:
        hanoi(n - 1, a, c, b)
        print('move from %s to %s' % (a, c))
        x += 1
        hanoi(n - 1, b, a, c)


hanoi(20, 'A', 'B', 'C')
print('move steps: %s' % x)