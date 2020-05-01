#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/6
# Location: DongGuang
# Desc:     do the right thing



"""
在定义的类中存在__del__方法时,
在程序执行完，当对象在内存中被回收(删除)前,程序会自动执行__del__当中的代码，
如果程序中有手动执行删除对象，则不会再执行__del__中的代码
(正好与__init__方法相反).
"""

class Foo:

    def __init__(self, name):
        self.name = name

    @staticmethod
    def bar():
        print('bar...')

    def __del__(self):
        print('del...')

f = Foo('jack')
print(id(f))  # 对象还在内存中
print('done')  # 程序执行完后，才会执行f.__del__()方法， 对f内存资源进行回收

del f  # 主动删除f对象
print(id(f))  # 报错；删除后无法再内存中找到，那么就不会在执行f.__del__()方法了