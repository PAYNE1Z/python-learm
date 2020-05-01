#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/10/30
# Location: DongGuang
# Desc:     do the right thing

"""
顺序查找：
    也叫线性查找，从列表第一个元素开始，顺序进行搜索，
    直到找到元素或搜索到列表最后一个元素为止
时间复杂度：
    将列表从头到尾只走了一遍，为 n，时间复杂度为：O(n)
"""


def linear_search(li, val):
    for idx, v in enumerate(li):
        if v == val:
            return idx
    else:
        return None


l = [1, 3, 5, 7, 9, 8, 6, 4, 2]

print(linear_search(l, 8))
