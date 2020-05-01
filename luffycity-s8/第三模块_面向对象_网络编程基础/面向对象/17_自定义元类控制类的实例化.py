#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/6
# Location: DongGuang
# Desc:     do the right thing



# 自定义一个元类：
class Mymeta(type):   # 所有用class定义的类的元类都是type, 所以这里要继承type类

    def __init__(cls, class_name, class_bases, class_dict):
        super(Mymeta, cls).__init__(class_name, class_bases, class_dict)

    def __call__(cls, *args, **kwargs):  # obj=Chinese('jack',sex='male')
        # cls:  Chinese
        # args: ('jack',)
        # kwargs: {'sex': 'male',}
        # __call__要做的三件事
        # 1、创建一个对象obj
        obj = object.__new__(cls)  # 创建一个对象本质都是通过基类object.__new__方法；obj=object.__new__(Chinese)
        # 2、初始化对象obj
        cls.__init__(obj, args, kwargs)  # Chinese.__init__(obj, 'jack', sex='male')
        # 3、返回对象obj
        return obj


# 定义一个基于元类Mymeta的类
class Chinese(object, metaclass=Mymeta):
    """
    中国人的类
    """
    country = 'china'

    def __init__(self, name, sex):
        self.name = name
        self.sex = sex

    def talk(self):
        print('{} is talking'.format(self.name))


# 实例化的过程实际上就是调用了实例化对象中的__call__方法
people = Chinese('jack', sex='male')   # obj = Chinese.__call__(Chinese, 'jack', sex='male')
print(people.__dict__)
people.talk()