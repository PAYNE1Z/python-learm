#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/4
# Location: DongGuang
# Desc:     do the right thing


"""
组合指的是，在一个类中以另外一个类的对象作为数据属性，称为类的组合
"""
class People:
    def __init__(self,name,age,sex):
        self.name=name
        self.age=age
        self.sex=sex

class Course:
    def __init__(self,name,period,price):
        self.name=name
        self.period=period
        self.price=price

    def tell_info(self):
        print('<%s %s %s>' %(self.name,self.period,self.price))

class Teacher(People):
    def __init__(self,name,age,sex,job_title):
        People.__init__(self,name,age,sex)
        self.job_title=job_title
        self.course=[]
        self.students=[]


class Student(People):
    def __init__(self,name,age,sex):
        People.__init__(self,name,age,sex)
        self.course=[]


egon=Teacher('egon',18,'male','沙河霸道金牌讲师')
s1=Student('牛榴弹',18,'female')

python=Course('python','3mons',3000.0)
linux=Course('python','3mons',3000.0)

# 为老师egon和学生s1添加课程
egon.course.append(python)  # egon.course = python; egon.course = linux
egon.course.append(linux)
s1.course.append(python)

# 为老师egon添加学生s1
egon.students.append(s1)  # egon.students = s1


# 使用
for obj in egon.course:
    obj.tell_info()