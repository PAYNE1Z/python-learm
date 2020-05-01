#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/13
# Location: DongGuang
# Desc:     通过yield实现在单线程的情况下实现并发运算的效果


import time


def consumer(name):
    """
    消费者
    :param name:
    :return:
    """
    while True:
        agg = yield
        agg += 1
        print('%s 捡到一个鸡蛋, [%s]' % (name, agg))
    return 'Done'


def produce(name, n_max):
    """
    生产者
    :param n_max:
    :param name:
    :return:
    """
    print('%s 开始生鸡蛋...' % name)
    for i in range(n_max):
        time.sleep(1.1)
        print('\n%s 生了两个蛋' % name)
        yield i
    return 'Done'


def main():
    c1 = consumer('jack')  # 初始化
    c2 = consumer('pony')
    p = produce('robin', 5)  # 生蛋
    c1.__next__()   # 唤醒生成器yield
    c2.__next__()

    for agg in p:
        c1.send(agg)
        c2.send(agg)


if __name__ == "__main__":
    main()

