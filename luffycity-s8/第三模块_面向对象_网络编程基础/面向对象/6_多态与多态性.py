#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/4
# Location: DongGuang
# Desc:     do the right thing


import abc

# 多态指的是一类事物有多种形态，比如 动物有多种形态：人，狗，猪
class Animal(metaclass=abc.ABCMeta):  # 同一类事物:动物
    @abc.abstractmethod
    def talk(self):
        pass

class People(Animal):  # 动物的形态之一:人
    def talk(self):
        print('say hello')

class Dog(Animal):  # 动物的形态之二:狗
    def talk(self):
        print('say wangwang')

class Pig(Animal):  # 动物的形态之三:猪
    def talk(self):
        print('say aoao')


# 多态性
peo=People()
dog=Dog()
pig=Pig()

# peo、dog、pig都是动物,只要是动物肯定有talk方法
# 于是我们可以不用考虑它们三者的具体是什么类型,而直接使用
peo.talk()
dog.talk()
pig.talk()

# 更进一步,我们可以定义一个统一的接口来使用
def func(obj):
    obj.talk()


# 鸭子类型
# Python崇尚鸭子类型，即‘如果看起来像、叫声像而且走起路来像鸭子，那么它就是鸭子’


# 例1：利用标准库中定义的各种‘与文件类似’的对象，尽管这些对象的工作方式像文件，但他们没有继承内置文件对象的方法
# 二者都像鸭子,二者看起来都像文件,因而就可以当文件一样去用，而不在需要再定义一个抽象类
class TxtFile:
    def read(self):
        pass

    def write(self):
        pass

class DiskFile:
    def read(self):
        pass

    def write(self):
        pass


# 例2：序列类型有多种形态：字符串，列表，元组，但他们直接没有直接的继承关系
# str,list,tuple都是序列类型，因而都可以使用len计算序列长度，而不在需要再定义一个抽象类
s=str('hello')
l=list([1,2,3])
t=tuple((4,5,6))

# 我们可以在不考虑三者类型的前提下使用s,l,t，
s.__len__()
l.__len__()
t.__len__()

len(s)
len(l)
len(t)