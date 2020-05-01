#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/4
# Location: DongGuang
# Desc:     do the right thing


"""
什么是特性property
    property是一种特殊的属性，访问它时会执行一段功能（函数）然后返回值

为什么要用property
    将一个类的函数定义成特性以后，对象再去使用的时候obj.name,
    根本无法察觉自己的name是执行了一个函数然后计算出来的，
    这种特性的使用方式遵循了统一访问的原则
"""


# 例一：BMI指数（bmi是计算而来的，但很明显它听起来像是一个属性而非方法，如果我们将其做成一个属性，更便于理解）
# 成人的BMI数值：
# 过轻：低于18.5
# 正常：18.5-23.9
# 过重：24-27
# 肥胖：28-32
# 非常肥胖, 高于32
# 体质指数（BMI）=体重（kg）÷身高^2（m）
# EX：70kg÷（1.75×1.75）=22.86


class People:
    def __init__(self, name, weight, height):
        self.name = name
        self.weight = weight
        self.height = height

    @property
    def bmi(self):
        return self.weight / (self.height ** 2)


p1 = People('jack', 90, 1.65)
# print(p1.bmi())  # 不加property的情况下，攻取值需要加()执行方法式的调用
print(p1.bmi)    # 加了property后，可以直接像取数据属性一样取值，使用者需要知道你内部执行了一个函数，只需要知道获取的是什么结果

if p1.bmi < 18.5:
    print('{}体重过轻，BMI:[{:.3f}]'.format(p1.name, p1.bmi))
elif p1.bmi <= 23.9:
    print('{}体重正常，BMI:[{:.3f}]'.format(p1.name, p1.bmi))
elif p1.bmi <= 27:
    print('{}体重过重，BMI:[{:.3f}]'.format(p1.name, p1.bmi))
elif p1.bmi <= 32:
    print('{}体重肥胖，BMI:[{:.3f}]'.format(p1.name, p1.bmi))
elif p1.bmi > 32:
    print('{}体重严重肥胖，快减肥吧，BMI:[{:.3f}]'.format(p1.name, p1.bmi))

# p1.bmi = 22.2  # 此时为特性bmi赋值会报错：AttributeError: can't set attribute



# 例二：圆的周长和面积

import math
class Circle:
    def __init__(self,radius):  # 圆的半径radius
        self.radius=radius

    @property
    def area(self):
        return math.pi * self.radius**2  # 计算面积

    @property
    def perimeter(self):
        return 2*math.pi*self.radius  # 计算周长

c=Circle(10)
print(c.radius)
print(c.area)  # 可以向访问数据属性一样去访问area,会触发一个函数的执行,动态计算出一个值
print(c.perimeter)  # 同上

# 输出结果:
# 314.1592653589793
# 62.83185307179586



"""
ps：面向对象的封装有三种方式:
【public】
这种其实就是不封装,是对外公开的
【protected】
这种封装方式对外不公开,但对朋友(friend)或者子类(形象的说法是“儿子”,
但我不知道为什么大家 不说“女儿”,就像“parent”本来是“父母”的意思,但中文都是叫“父类”)公开
【private】
这种封装对谁都不公开

python并没有在语法上把它们三个内建到自己的class机制中，
在C++里一般会将所有的所有的数据都设置为私有的，然后提供set和get方法（接口）去设置和获取，
在python中通过property方法可以实现
"""

# 例三：
class Foo:
    def __init__(self,val):
        self.__NAME=val  # 将所有的数据属性都隐藏起来

    @property   # 查看
    def name(self):
        return self.__NAME  # obj.name访问的是self.__NAME(这也是真实值的存放位置)

    @name.setter  # 修改
    def name(self,value):
        if not isinstance(value,str):  # 在设定值之前进行类型检查
            raise TypeError('%s must be str' %value)
        self.__NAME=value  # 通过类型检查后,将值value存放到真实的位置self.__NAME

    @name.deleter  # 删除
    def name(self):
        raise TypeError('Can not delete')

f=Foo('egon')
print(f.name)
# f.name=10  # 抛出异常'TypeError: 10 must be str'
del f.name  # 抛出异常'TypeError: Can not delete'