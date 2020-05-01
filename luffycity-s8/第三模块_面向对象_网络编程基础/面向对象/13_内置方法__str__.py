#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/6
# Location: DongGuang
# Desc:     do the right thing


"""
当使用print输出对象的时候，
只要自己定义了__str__(self)方法，
那么就会打印从在这个方法中return的数据
"""


class Cat:
    """定义了一个Cat类"""

    # 初始化对象
    def __init__(self, new_name, new_age):
        self.name = new_name
        self.age = new_age

    def __str__(self):
        return "%s的年龄是:%d" % (self.name, self.age)

    # 方法
    @staticmethod
    def eat():
        print("猫在吃鱼....")

    @staticmethod
    def drink():
        print("猫正在喝kele.....")

    def introduce(self):
        print("%s的年龄是:%d" % (self.name, self.age))


# 创建一个对象
tom = Cat("汤姆", 40)
mao = Cat("蓝猫", 10)

tom.eat()
mao.eat()

print(tom)  # print的时候执行:  tom.__str__()
print(mao)  # print的时候执行:  mao.__str__()
