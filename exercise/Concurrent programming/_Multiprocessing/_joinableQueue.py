#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/29
# Location: DongGuang
# Desc:     JoinableQueue的应用


from multiprocessing import JoinableQueue, Process
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
    qp.join()  # 等到消费者把自己放入队列中的所有的数据都取走之后，生产者才结束


def consumer(qc, name):
    """消费者
    :param qc: 队列对象
    :param name: 消费者名称
    """
    while True:
        time.sleep(random.random())
        food = qc.get()
        # if food is None: break   # 接收到生产结束信号
        print(f'[{name}]购买了: [{food}]')
        qc.task_done()  # 发送信号给生产者的q.join()，说明已经从队列中取走一个数据并处理完毕了


if __name__ == "__main__":
    q = JoinableQueue()

    p1 = Process(target=producer, args=(q, '娃哈哈', '旺旺雪饼', 3))
    p2 = Process(target=producer, args=(q, '家多宝', '凉茶', 2))
    p3 = Process(target=producer, args=(q, '徐福记', '糖果', 4))

    c1 = Process(target=consumer, args=(q, '老王'))
    c2 = Process(target=consumer, args=(q, '小明'))
    c3 = Process(target=consumer, args=(q, '马云'))
    c4 = Process(target=consumer, args=(q, '三毛'))

    producer_list = [p1, p2, p3]
    consumer_list = [c1, c2, c3, c4]

    for p in producer_list:
        p.start()   # 启动生产者
    for c in consumer_list:
        c.daemon = True  # 将消费者设为守护进程, 当所有生产者结束，主进程结束后，消费者也将自动结束，不用再发结束信号了
        c.start()        # 启动消费者

    for p in producer_list:
        p.join()    # 确保生产者生产完了所有商品, 并且q.join()了

    # for i in range(len(consumer_list)):
    #     q.put(None)  # 给消费者发送结束信号
    print('done')