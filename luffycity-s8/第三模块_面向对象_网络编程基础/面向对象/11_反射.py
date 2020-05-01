#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/5
# Location: DongGuang
# Desc:     do the right thing


"""
反射：通过字符串映射到对象的属性
"""

class Foo:
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex

    @staticmethod
    def talk():
        print('is talking')

f = Foo('jack', 53, 'male')


print(hasattr(f, 'name'))  # if f.name 判断对象或类中是否有'name'属性
# True

print(getattr(f, 'name', None))  # f.name 获取对象或类中的'name'属性,
# jack
print(getattr(f, 'addr', None))  # 加上None参数，当属性不存在就返回None
# None

setattr(f, 'name', 'pony')  # f.name = 'pony' 修改或新增对象或类中的'name'属性
setattr(f, 'phone', 13933993399)  # f.phone = 13933993399
print(f.name, f.phone)
# pony 13933993399

delattr(f, 'phone')  # del f.phone 删除对象或类中的'phone'属性
print(hasattr(f, 'phone'))
# False


# 反射的应用
# 新增一个服务类，根据用户输入的字符串运行相应的功能
# eg. 输入'get' 就执行 Service.get()
class Service:
    def run(self):
        while True:
            cmds = input('>>:').strip().split()
            if hasattr(self, cmds[0]):
                func = getattr(self, cmds[0])
                func(cmds)

    @staticmethod
    def get(cmds):
        print('get...', cmds)

    @staticmethod
    def put(cmds):
        print('put...', cmds)


s = Service()
s.run()