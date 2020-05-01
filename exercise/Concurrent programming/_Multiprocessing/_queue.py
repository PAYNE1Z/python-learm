#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/29
# Location: DongGuang
# Desc:     Queue的应用


"""
使用生产者消费者模型，模拟一个生产者一个消费者，之前数据通过Queue存储与传输
"""
from multiprocessing import Queue, Process
import time
import random


def producer(qp, name, food, count):
    """生产者
    :param qp: 队列对象
    :param name： 生产者名称
    :param food: 生产者生产的产品
    :param count: 生产数据
    """
    for n in range(count):
        time.sleep(random.random())
        food_num = f'{food}{n}'
        print(f'[{name}]生产了[{food_num}]')
        qp.put(food_num)


def consumer(qc, name):
    """消费者
    :param qc: 队列对象
    :param name: 消费者名称
    """
    while True:
        time.sleep(random.random())
        food = qc.get()
        if food is None: break   # 接收到生产结束信号
        print(f'[{name}]购买了: [{food}]')


if __name__ == "__main__":
    q = Queue()

    p1 = Process(target=producer, args=(q, '娃哈哈', '旺旺雪饼', 6))
    p2 = Process(target=producer, args=(q, '家多宝', '凉茶', 5))
    p3 = Process(target=producer, args=(q, '徐福记', '糖果', 8))

    c1 = Process(target=consumer, args=(q, '老王'))
    c2 = Process(target=consumer, args=(q, '小明'))
    c3 = Process(target=consumer, args=(q, '马云'))
    c4 = Process(target=consumer, args=(q, '三毛'))

    producer_list = [p1, p2, p3]
    consumer_list = [c1, c2, c3, c4]

    for p in producer_list:
        p.start()   # 启动生产者
    for c in consumer_list:
        c.start()   # 启动消费者

    for p in producer_list:
        p.join()    # 确保生产者生产完了所有商品

    for i in range(len(consumer_list)):
        q.put(None)  # 给消费者发送结束信号，有几个消费者就要发送几个