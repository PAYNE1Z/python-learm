#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/3
# Location: DongGuang
# Desc:     do the right thing


"""
练习1： 编写一个学生类，产生一堆学生对象
要求：
    有一个计数器(属性), 统计总共实例了多少个对象
"""

class Student:
    school = 'Luffycity'  # 类的数据属性，所有对象都能访问(通过各对象来访问可以发现，各对象访问数据属性的内存地址是一样的)
    count = 0  # 计数器

    def __init__(self, name, age, sex):   # __init__方法用于接收生成对象的私有属性
        self.name = name
        self.age = age
        self.sex = sex
        Student.count += 1
        # 因为每创建对象对会自动执行__init__函数，所以直接在__init__函数中对类的变量操作,累加实例次数

    def learn(self):  # 类的函数属性，绑定到对象后，对象使用(通过各对象来访问可以发现，各对象调用的函数属性是独立的)
        print('{} is learning'.format(self.name))

    def eat(self):
        print('{} is eating'.format(self.name))


stu1 = Student('jack', 52, 'male')  # 创建对象(实例化)
stu2 = Student('pony', 45, 'male')
stu3 = Student('robin', 47, 'male')
print('{}共实例了{}个对象'.format(Student.__name__, Student.count))


