#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/6
# Location: DongGuang
# Desc:     do the right thing


"""
储备知识：exec
    参数1：字符串形式的命令
    参数2：全局作用域(字典形式)，如果不指定默认就使用 globals()
    参数3：局部作用域(字典形式), 如果不指定默认就使用 locals()

python中一切皆对象，对象可以怎么用？
    1、都可以被引用，如：x=obj obj可以是各种数据类型或函数或类
    2、都可当作函数的参数传入, 如：func(args) args可以是各种数据类型或函数或类
    3、都可以当作函数的返回值，如：return obj obj可以是各种数据类型或函数或类
    4、都可以当作容器元素，如 l=[obj] obj可以是各种数据类型或函数或类
    只要是对象，就符合以上特点，这就是一切皆对象，是一种统一的思想

元类：
    元类是类的类，是类的模板
    元类是用来控制如何创建类的，正如类是创建对象的模板一样，而元类的主要目的是为了控制类的创建行为
    元类的实例化的结果为我们用class定义的类，正如类的实例为对象(f1对象是Foo类的一个实例，Foo类是 type 类的一个实例)
    type是python的一个内建元类，用来直接控制生成类，python中任何class定义的类其实都是type类实例化的对象


type 接收三个参数：
第 1 个参数是字符串 ‘Foo’，表示类名
第 2 个参数是元组 (object, )，表示所有的父类
第 3 个参数是字典，这里是一个空字典，表示没有定义属性和方法
补充：若Foo类有继承，即class Foo(Bar):.... 则等同于type('Foo',(Bar,),{})
"""


# 定义类的两种方式：
# 1、使用class
class Chinese:
    country = 'China'

    def __init__(self, name):
        self.name = name

    def talk(self):
        print('{} talking'.format(self.name))

print(Chinese)
people = Chinese('jack')
print(people, people.name, people.talk())


# 2、使用元类type
# 定义类的三要素：类名，类的基类们，类的名称空间
class_name = 'Chinese1'  # 类名
class_bases = (object,)  # 类的基类们（所有类都会继承object类，所以object类是所有类的基类)

class_body = """     # 类中的属性（数据与方法）
country = 'China'

def __init__(self, name):
    self.name = name
    
def talk(self):
    print('{} talking'.format(self.name))
"""
class_dict = {}     # 类的名称空间
exec(class_body, globals(), class_dict)   # 使用exec将类中的属性写入类的局部空间
Chinese1 = type(class_name, class_bases, class_dict)  # 使用元类type定义一个类

print(Chinese1)
people1 = Chinese1('jack')   # 实例化对象
print(people1, people1.name, people1.talk())  # 读取对象属性