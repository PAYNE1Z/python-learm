#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/6
# Location: DongGuang
# Desc:     do the right thing


# 实现单例模式（相同特性的对象只创建一个）

# 方式一：类中定义方法
class MySQL:
    __instance = None

    def __init__(self):
        self.host = 'localhost'
        self.port = 3306

    @classmethod
    def singleton(cls):
        if not cls.__instance:
            obj = cls()
            cls.__instance = obj
        return cls.__instance

    def conn(self):
        pass

    def execute(self):
        pass

# 通过类实例化
my1 = MySQL()
my2 = MySQL()
my3 = MySQL()
print(my1 is my2 is my3)  # False  是三个不同的对象

# 通过类中定义的方法实例化
my1 = MySQL.singleton()
my2 = MySQL.singleton()
my3 = MySQL.singleton()
print(my1 is my2 is my3)  # True 三个对象是一样的


# 方式2、通过元类实现
class Mymeta(type):
    def __init__(cls, *args, **kwargs):
        super(Mymeta, cls).__init__(cls, args, kwargs)  # 继承属性
        cls.__instance= None

    def __call__(cls, *args, **kwargs):
        if not cls.__instance:
            obj = object.__new__(cls)  # 创建空对象
            cls.__init__(obj)          # 初始化空对象
            cls.__instance = obj
        return cls.__instance          # 返回对像


class Mysql(object,metaclass=Mymeta):
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306

    def conn(self):
        pass

    def execute(self):
        pass


# 通过元类Mymeta.__call__方法实例化
my1 = Mysql()
my2 = Mysql()
my3 = Mysql()
print(my1 is my2 is my3)  # True