#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/6
# Location: DongGuang
# Desc:     do the right thing



# 练习：
# 1.元类帮其完成创建对象，以及初始化操作；
# 2.要求实例化时传参必须为关键字形式，否则抛出异常TypeError: must use keyword argument
# 3.key作为用户自定义类产生对象的属性，且所有属性变成大写


class Mymeta(type):
    def __new__(mcs, name, bases, attrs):  # 元类中对象本身用mcs表示：__new__(Mymeta, 'People', (object,), People.__dict__)
        new_dict = {}
        for k, v in attrs.items():
            if not callable(v) and not k.startswith('__'):  # 方法与特殊属性不用转换
                new_dict[k.upper()] = v
            else:
                new_dict[k] = v
        return type.__new__(mcs, name, bases, new_dict)  # 使用继承的元类type创建name类对象

    def __call__(cls, *args, **kwargs):   # cls: People
        if args:   # 以关键字形式传参，那么args接收的参数应该要为空，都在kwargs接收
            raise TypeError('must use keyword argument')
        obj = object.__new__(cls)   # 使用基类创建类对象
        for key, value in kwargs.items():
            obj.__dict__[key.upper()] = value     # 对象数据属性变量名改成大写

        return obj


# People继承于Mymeta元类，会先执行Mymeta.__new__()方法
class People(metaclass=Mymeta):  # People = Mymeta.__new__(Mymeta, 'People', (object,), People.__dict__)
    country = 'China'
    tag = 'legend of the Dragon'

    def walk(self):
        print('{} is walking...'.format(self.__dict__['name']))


# People类将会在People()调用时，执行Mymeta元类中的__call__方法
people = People(name='jack', age=53)  # people = Mymeta.__call__(People, name='jack', age=15)


for k, v in People.__dict__.items():
    if not callable(v) and not k.startswith('__'):
        print('{}:{}'.format(k, People.__dict__[k]))
# TAG:legend of the Dragon
# COUNTRY:China

for k, v in people.__dict__.items():
    if not callable(v) and not k.startswith('__'):
        print('{}:{}'.format(k, people.__dict__[k]))
# NAME:jack
# AGE:53