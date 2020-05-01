#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/9
# Location: DongGuang
# Desc:     递归


import sys

# python对递归循环次数有安全限制为1000次，1000次后会报错
# 可以通过以下方法查询限制数或修改限制次数
sys.getrecursionlimit()
sys.setrecursionlimit(1100)

# 死循环
def recursion(n):
    print(n)
    recursion(n+1)

# recursion(0)

"""
递归函数：就是函数在内部调用函数本身，那这个函数就是递归函数
递归特性:
1、必须有一个明确的结束条件
2、每次进入更深一层递归时，问题规模相比上次递归都应有所减少
3、递归效率不高，递归层次过多会导致栈溢出
   在计算机中，函数调用是通过栈（stack）这种数据结构实现的，
   每当进入一个函数调用，栈就会加一层栈帧，
   每当函数返回，栈就会减一层栈帧。
   由于栈的大小不是无限的，所以，递归调用的次数过多，会导致栈溢出
"""

def calc(n):
    print(n)
    if int(n/2) == 0:
        return n
    return calc(int(n/2))

# calc(10)


def calc2(n):
    v = int(n/2)
    # 这个打印语句位于调用自身函数前面，
    # 所有每进入一层就会打印
    print('first:', v)
    if v > 0:
        calc2(v)  # 进入下层函数
    print('second:', v)
    # 这个打印语句位于调用自身函数后面，
    # 所以要等所有下层函数调用结束才开始向外一层一层打印

# calc2(10)
# 返回如下(为什么第二个v没有跟在第一个v前面打印，并且数值也不一样?)
# first: 5
# first: 2
# first: 1
# first: 0
# second: 0
# second: 1
# second: 2
# second: 5


# 用递归实现阶乘 n! = n * (n-1)!
# 10! = 10 * (10-1)!

def factorial(n):
    if n == 1:
        return 1
    # 这个操作感觉非常骚气，一脸懵逼
    return n * factorial(n-1)

print(factorial(5))
# 现在通过一层一层来看看这波操作
# ===> factorial(5)
# ===> 5 * factorial(4)
# ===> 5 * (4 * factorial(3))
# ===> 5 * (4 * (3 * factorial(2)))
# ===> 5 * (4 * (3 * (2 * factorial(1))))   # 到这里里层函数退出时，开始层层计算
# ===> 5 * (4 * (3 * (2 * 1)))
# ===> 5 * (4 * (3 * 2))
# ===> 5 * (4 * 6)
# ===> 5 * 24
# ===> 120



# 用递归函数实现二分查找

data = [1, 3, 6, 7, 9, 12, 14, 16, 17, 18, 20, 21, 22, 23, 30, 32, 33, 35]

def binary_search(data_set, num):
    """
    使用二分查找查看某数字是否存在于列表中
    :param data_set: 数据集
    :param num: 要查找的数值
    :return:
    """
    print(data_set, num)

    if len(data_set) > 1:  # 数据集中有1个数以上
        num_index = int(len(data_set)/2)  # 找到列表中位数的索引
        if data_set[num_index] == num:   # 中位数等于要查找的数
            print('找到了，%s在数据集中' % num)
        elif data_set[num_index] > num:  # 中位数大于要查找的数
            print('要找的数在%s左边' % data_set[num_index])
            return binary_search(data_set[0:num_index], num)  # 将中位数左边的数据集进行递归查找
        else:  # 中位数小于要查找的数
            print('要找的数在%s右边' % data_set[num_index])
            return binary_search(data_set[num_index+1:], num)  # 将中位数右边的数据集进行递归查找
    else:  # 数据集中只有1个数了
        if data_set[0] == num:
            print('找到了，%s在数据集中' % num)
        else:
            print('%s不在数据集中' % num)

binary_search(data, 32)
