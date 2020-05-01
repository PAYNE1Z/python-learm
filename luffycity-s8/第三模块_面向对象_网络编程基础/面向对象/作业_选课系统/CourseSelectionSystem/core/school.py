#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/24
# Location: DongGuang
# Desc:     各对象的类


import time
from modules.new_input import new_input
from modules.check_obj_exist import is_exist


class School:
    """学校类"""
    school_name = 'LuffyCity'

    def __init__(self, addr):
        """
        :param addr: 学校校区
        """
        self.addr = addr
        self.courses = []
        self.teachers = []
        self.classes = []
        self.students = []

    def __str__(self):
        return """校区: [{}]
        班级：{} 
        课程: {}
        老师: {}
        学生: {}""".format(self.addr, self.classes, self.courses, self.teachers, self.students)

    def select_obj(self, data, obj_type):
        """
        选择对象
        :param data: 对象数据集
        :param obj_type: 要选择的对象类型 ['schools', 'teachers', 'courses', 'classes', 'students']
        :return obj
        """
        obj_map = {
            'schools': '校区',
            'teachers': '老师',
            'courses': '课程',
            'classes': '班级',
            'students': '学生'
        }
        if self.show_obj(data):
            obj_name = new_input('请选择[{}]>>>: '.format(obj_map[obj_type]))
            if is_exist(obj_name, data, 'in'):
                return data[obj_name]
            else:
                return False

    @staticmethod
    def show_obj(data):
        """
        打印各对象信息
        :param data: 对象数据字典
        """
        if data:
            for num, obj in enumerate(data, 1):
                print('{}. '.format(num), data[obj])
            print(''.center(30, '+'))
            return True
        else:
            print('还没有数据')
            return False

    @staticmethod
    def create_course(name, period, price):
        """创建课程"""
        course_obj = Course(name, period, price)
        return course_obj

    @staticmethod
    def create_teacher(name, salary, school_addr):
        """创建老师"""
        teacher_obj = Teacher(name, salary, school_addr)
        return teacher_obj

    @staticmethod
    def create_classes(name, school_addr, course_name):
        """创建班级"""
        classes_obj = Classes(name, school_addr, course_name)
        return classes_obj


class Classes(School):
    """班级类： 一个班级绑定一门课程，一个老师，多个学生"""
    def __init__(self, name, school_addr, course_name):
        self.name = name
        self.school_addr = school_addr
        self.course_name = course_name
        self.teacher_name = None
        self.students = []

    def __str__(self):
        return """班级名称：{}
        所属校区：{}
        课程: {}
        老师：{}
        学员：{}""".format(self.name, self.school_addr, self.course_name, self.teacher_name, self.students)


class Course(School):
    """课程类"""
    def __init__(self, name, period, price):
        self.name = name
        self.period = period
        self.price = price

    def __str__(self):
        return """课程名称：{}
        课程周期: {}
        课程费用：{}""".format(self.name, self.period, self.price)


class Teacher(School):
    """老师类"""
    def __init__(self, name, salary, school_addr):
        self.name = name
        self.salary = salary
        self.school_addr = school_addr
        self.classes = []

    def __str__(self):
        return """老师名称: {}
        薪酬: {}
        所属校区: {}
        授课班级: {}""".format(self.name, self.salary, self.school_addr, self.classes)


class Student(School):
    """学员类"""
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex
        self.reg_date = time.strftime('%Y-%m-%d', time.localtime())
        self.classes_name = None
        self.teacher_name = None
        self.course_name = None
        self.score = None
        self.pay_status = False

    def __str__(self):
        return """学生姓名: {}
        年龄: {}
        性别: {}
        注册时间: {}
        所属班级: {}
        班级老师: {}
        班级课程: {}
        课程成绩: {}
        缴费状态: {}""".format(
            self.name, self.age, self.sex, self.reg_date, self.classes_name,
            self.teacher_name, self.course_name, self.score, self.pay_status
        )