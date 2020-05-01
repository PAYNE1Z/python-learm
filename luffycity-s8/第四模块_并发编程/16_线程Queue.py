#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/1
# Location: DongGuang
# Desc:     do the right thing

"""
queue.Queue(maxsize=0)         #队列：先进先出
queue.LifoQueue(maxsize=0)     #堆栈：last in fisrt out
queue.PriorityQueue(maxsize=0) #优先级队列：存储数据时可设置优先级的队列
"""

import queue

# 队列：先进先出
q1 = queue.Queue(3)   #  maxsize: 设定队列最多能存多少个值
q1.put(1)
q1.put(2)
q1.put(3)
# q1.put(4)  # 默认block=True 超过3个值时这里会卡住，等到有值被get才能入列
# q1.put(4, block=False)  # 设置block=False,将会触发异常退出
# q1.put(4, block=True, timeout=3)  # 设置block=True, 将在timeout时间后(仍然没有值被get)触发异常退出

print(q1.get())
print(q1.get())
print(q1.get())
# print(q1.get(block=False))   # 队列为空时，触发异常退出
# print(q1.get_nowait())   # 等同get(block=False)
# print(q1.get(block=True, timeout=3))   # 队列为空时，将在timeout时间后(仍然没有值put入列)触发异常退出


# 堆栈: 先进后出 last in first out
q2 = queue.LifoQueue(3)
q2.put('一')
q2.put('二')
q2.put('三')
print(q2.get())
print(q2.get())
print(q2.get())


# 优先级队列:
q3 = queue.PriorityQueue(3)
q3.put((5, 'one'))   # put数据时，以元组形式，第一个值为优先级(数字越小优先级越高)， 第二个值为要入列的数据
q3.put((2, 'two'))
q3.put((9, 'three'))
print(q3.get())
print(q3.get())
print(q3.get())