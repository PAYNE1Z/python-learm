#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/29
# Location: DongGuang
# Desc:     Queue的使用


from multiprocessing import Queue


q = Queue(maxsize=3)   # maxsize: 是队列中允许最大项数，省略则无大小限制

# 往队列写入数据
q.put('Hello')
q.put({'a': 1})
q.put([1, 2, 3])

# 检测队列是否已满
print(q.full())
# 队列已满的情况下再put,程序会卡住，等待数被取出有空间后才能插入
# q.put('full')

# 从队列读取数据，并删除读取的元素
print(q.get())
print(q.get())
print(q.get())

# 检测队列是否已空
print(q.empty())
# 队列已空的情况下再get,程序会卡住，等待有新的数据进入队列才能取得
# print(q.get())