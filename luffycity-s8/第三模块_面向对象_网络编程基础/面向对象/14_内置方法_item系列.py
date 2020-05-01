#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/5
# Location: DongGuang
# Desc:     do the right thing


"""
item系列： 让类的属性以字典的形式操作
__getitem__(self,item)
__setitem__(self,key,value)
__delitem__(self,key)
"""

class Foo:
    def __init__(self, name):
        self.name = name

    def __getitem__(self, item):
        print(self.__dict__.get(item))
        print("obj[{}] 的时候执行...".format(item))

    def __setitem__(self, key, value):
        # self.key = value
        self.__dict__[key] = value
        print("obj[{}]={} 的时候执行...".format(key, value))

    def __delitem__(self, key):
        # del self.key
        del self.__dict__[key]
        print('del obj[{}] 的时候执行...'.format(key))


f = Foo('JackMa')

print(f['name'])
# JackMa
# obj[name] 的时候执行...
# None

f['name'] = 'PonyMa'
print(f.name)
# obj[name]=PonyMa 的时候执行...
# JackMa

f['age'] = 53
# obj[age]=53 的时候执行...
del f['age']
# del obj[age] 的时候执行...
# None
print(f['age'])
# obj[age] 的时候执行...
# None