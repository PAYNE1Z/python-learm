#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/4
# Location: DongGuang
# Desc:     do the right thing



import abc

"""
如果说类是从一堆对象中抽取相同的内容而来的，那么抽象类就是从一堆类中抽取相同的内容而来的，
内容包括数据属性和函数属性。

比如我们有香蕉的类，有苹果的类，有桃子的类，从这些类抽取相同的内容就是水果这个抽象的类，
你吃水果时，要么是吃一个具体的香蕉，要么是吃一个具体的桃子。。。。。。
你永远无法吃到一个叫做水果的东西。

从设计角度去看，如果类是从现实对象抽象而来的，那么抽象类就是基于类抽象而来的。
从实现角度来看，抽象类与普通类的不同之处在于：
抽象类中只能有抽象方法（没有实现功能），该类不能被实例化，只能被继承，且子类必须实现抽象方法
"""

class Animal(metaclass=abc.ABCMeta):  # 定义一个抽象类： 抽象类只能被继承，不能被实例化
    all_type = 'animal'

    @abc.abstractmethod
    def eat(self):   # 抽象方法，功能由其子类实现
        pass

    @abc.abstractmethod
    def run(self):
        pass

# animal = Animal()  # 会报错，抽象类不能被实例化
# TypeError: Can't instantiate abstract class Animal with abstract methods eat, run


class People(Animal):  # 抽象类的子类，必须实现抽象类中的抽象方法 eat,run
    def eat(self):
        print('people is eating')

    def run(self):
        print('people is running')

# p1 = People()  # 子类中如果没有实现抽象方法会报错
# TypeError: Can't instantiate abstract class People with abstract methods eat, run


class Pig(Animal):
    def eat(self):
        print('pig is eating')

    def run(self):
        print('pig is running')


class Dog(Animal):
    def eat(self):
        print('dog is eating')

    def run(self):
        print('dog is running')


people1 = People()  # 实例化
pig1 = Pig()
dog1 = Dog()

people1.eat()  # 调用方法
pig1.eat()
dog1.eat()
people1.run()
pig1.run()
dog1.run()
print(people1.all_type)
print(pig1.all_type)
print(dog1.all_type)


