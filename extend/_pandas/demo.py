#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/26
# Location: DongGuang
# Desc:     do the right thing

import pandas as pd
import numpy as np

np.random.seed(1)  # 设置seed, 那么通过random取随机数时，每次取到的随机数将是一样的
s1 = pd.Series(np.random.randint(size=5, low=1, high=10))
print(s1, '\n')

print('**** 取第一个元素 ****')
print(s1[0], '\n')
print('**** 取第2~3个元素 ****')
print(s1[1:3], '\n')
print('**** 依次取元素，步长为2 ****')
print(s1[::2], '\n')

print('倒数取元素(简洁并高速)：')
print(s1)
print(s1.iat[-3], '\n')
print(s1[-3:], '\n')


print('布尔索引：')
s2 = pd.Series(np.random.randint(size=5, low=1, high=100))
print(s2)
# 取出>=70的值
print(s2[s2 >= 70])
# 取出10到50之间的值
print('------')
print(s2[s2 >= 10][50 >= s2])


# 一个向量的元素是否包含于另一个向量  np.in1d
arr1 = np.array([1,2,3,4])
arr2 = np.array([10,20,3,40])
print(np.in1d(arr1,arr2),'\n')

s1 = pd.Series(['A','B','C','D'])
s2 = pd.Series(['X','A','Y','D'])
print('s1 是否包含于 s2中')
print(s1.isin(s2), '\n')
print(np.in1d(s1,s2),'\n')