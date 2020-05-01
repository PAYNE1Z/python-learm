#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/6
# Location: DongGuang
# Desc:     do the right thing

"""
一个类没有声明自己的元类，默认他的元类就是type，除了使用元类type，
用户也可以通过继承type来自定义元类（顺便我们也可以瞅一瞅元类如何控制类的行为，工作流程是什么)
"""

# 自定义一个元类：
class Mymeta(type):   # 所有用class定义的类的元类都是type, 所以这里要继承type类

    def __init__(cls, class_name, class_bases, class_dict):
        # 在元类中规范新建的类名首字母要大写
        if not class_name.istitle():
            raise TypeError('类名首字母一定要大写')

        # 在元类中规范新建的中一定要有说明注释，并且内容不能为空
        if '__doc__' not in class_dict or not class_dict['__doc__'].strip():
            raise TypeError('类中一定要有说明注释，并且内容不能为空')
            # __doc__ 为类中的注释说明，如果没写注释名称空间中将不会有这个key

        super(Mymeta, cls).__init__(class_name, class_bases, class_dict)



# 定义一个基于元类Mymeta的类
class Chinese(object, metaclass=Mymeta):
    """
    中国人的类
    """
    country = 'china'

    def __init__(self, name):
        self.name = name

    def talk(self):
        print('{} is talking'.format(self.name))


people = Chinese('jack')
print(Chinese.__dict__)
print(people, people.name)
people.talk()