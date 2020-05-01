#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/30
# Location: DongGuang
# Desc:     管理员视图


from conf import settings
from modules.serialization import Serialize
from modules.is_number import is_number
from modules.generate_obj_data import generate
from modules.make_account import make_account
from core.school import *


class ManagerView(School):
    """管理员"""
    func_list = [
        ('创建学校', 'add_school'),
        ('创建课程', 'add_course'),
        ('创建老师', 'add_teacher'),
        ('创建班级', 'add_classes'),
        ('创建登录帐号', 'add_account'),
        ('查看所有校区', 'show_schools'),
        ('查看所有课程', 'show_courses'),
        ('查看所有老师', 'show_teachers'),
        ('查看所有班级', 'show_classes'),
        ('查看所有学生', 'show_students'),
        ('查看所有帐户', 'show_account_info'),
        ('退出', 'exit_func')
    ]

    def __init__(self, name):
        self.name = name

    @classmethod
    def show_schools(cls):
        """查看所有校区"""
        print("[{}]校区信息".format(super().school_name).center(30, '+'))
        super().show_obj(settings.SCHOOLS_DATA)

    @classmethod
    def show_classes(cls):
        """查看班级信息"""
        print("班级信息".center(30, '+'))
        super().show_obj(settings.CLASSES_DATA)

    @classmethod
    def show_teachers(cls):
        """查看老师信息"""
        print("老师信息".center(30, '+'))
        super().show_obj(settings.TEACHERS_DATA)

    @classmethod
    def show_courses(cls):
        """查看课程信息"""
        print('课程信息'.center(30, '+'))
        super().show_obj(settings.COURSES_DATA)

    @classmethod
    def show_students(cls):
        """查看学生信息"""
        print('学生信息'.center(30, '+'))
        super().show_obj(settings.STUDENTS_DATA)

    @staticmethod
    def add_account():
        """创建登录帐号"""
        make_account()

    @staticmethod
    def add_school():
        """创建学校"""
        addr = new_input('请设置校区名称>>>: ')
        if addr not in settings.SCHOOLS_DATA:         # 学校不存在才创建
            school_obj = School(addr)
            settings.SCHOOLS_DATA[addr] = school_obj  # 更新学校数据字典
            print('[{}]校区创建成功'.format(addr))
        else:
            print('[{}]校区已存在'.format(addr))

    def add_course(self):
        """创建课程：通过学校创建课程：课程可以在多个班级，也可以在多个校区"""
        school_obj = self.select_obj(settings.SCHOOLS_DATA, 'schools')
        if school_obj:
            course_name = new_input('请设置课程名称>>>: ')
            if course_name in settings.COURSES_DATA:               # 课程对象已存在
                if not is_exist(course_name, school_obj.courses):  # 并且还未加入学校
                    choice = input('[{}]课程对象已存在，直接加到学校请按[Y|y]>>>:'.format(course_name))
                    if choice.upper() == 'Y':
                        school_obj.courses.append(course_name)
                        print('[{}]课程成功加入[{}]校区'.format(course_name, school_obj.addr))
            else:  # 课程对象不存在就创建
                course_period = new_input('请设置课程周期>>>: ')
                course_price = is_number(new_input('请设置课程费用>>>: '))
                if course_price:
                    course_obj = school_obj.create_course(course_name, course_period, course_price)
                    settings.COURSES_DATA[course_name] = course_obj  # 加到课程数据字典
                    school_obj.courses.append(course_name)           # 课程加到校区课程列表
                    print('[{}]课程创建成功'.format(course_name))
            settings.SCHOOLS_DATA[school_obj.addr] = school_obj      # 更新学校数据字典

    def add_teacher(self):
        """新增老师：通过学校新增老师：一个老师只能在一个校区，可以有多个班级"""
        school_obj = self.select_obj(settings.SCHOOLS_DATA, 'schools')
        if school_obj:
            teacher_name = new_input('请设置老师名称>>>: ')
            if not is_exist(teacher_name, settings.TEACHERS_DATA):
                teacher_salary = is_number(new_input('请设置老师薪酬>>>: '))
                if teacher_salary:
                    teacher_obj = school_obj.create_teacher(teacher_name, teacher_salary, school_obj.addr)
                    settings.TEACHERS_DATA[teacher_name] = teacher_obj   # 更新老师数据字典
                    school_obj.teachers.append(teacher_name)             # 把老师加到对应的校区
                    settings.SCHOOLS_DATA[school_obj.addr] = school_obj  # 更新学校数据字典
                    # 每创建一个老师对象需要给老师设置一个管理登录帐号，用来管理老师的班级
                    make_account(teacher_name, 'Teacher')
                    print('[{}]老师创建成功'.format(teacher_name))

    def add_classes(self):
        """新增班级：通过学校创建班级：一个班级只在一个校区，一门课程"""
        school_obj = self.select_obj(settings.SCHOOLS_DATA, 'schools')
        if school_obj:
            classes_name = new_input('请设置班级名称>>>: ')
            if not is_exist(classes_name, settings.CLASSES_DATA):
                # 选择当前学校中的课程
                course_obj = self.select_obj(generate(settings.COURSES_DATA, school_obj.courses), 'courses')
                if course_obj:
                    classes_obj = school_obj.create_classes(classes_name, school_obj.addr, course_obj.name)  # 创建班级对象
                    classes_obj.course_name = course_obj.name  # 课程绑定到班级
                    school_obj.classes.append(classes_name)  # 班级加到校区班级列表
                    settings.CLASSES_DATA[classes_name] = classes_obj    # 更新班级对象数据
                    settings.SCHOOLS_DATA[school_obj.addr] = school_obj  # 更新学校对象数据
                    settings.COURSES_DATA[course_obj.name] = course_obj  # 更新课程对象数据
                    print('[{}]班级创建成功'.format(classes_name))

    @staticmethod
    def show_account_info():
        """查看帐户信息"""
        user_type = new_input('请输入要查看的帐户的类型[{}]>>>: '.format('|'.join(settings.USER_TYPE_LIST)))
        num = 0
        if user_type in settings.USER_TYPE_LIST:
            print('[{}]帐户信息'.format(user_type).center(30, '+'))
            for account in settings.ACCOUNTS_DATA:
                if settings.ACCOUNTS_DATA[account]['type'] == user_type:
                    num += 1
                    print('{}. name: [{}]; info: {}'.format(num, account, settings.ACCOUNTS_DATA[account]))
            if num == 0:
                print('还没有[{}]类型帐户'.format(user_type))
        else:
            print('错误的帐户类型')

    @staticmethod
    def exit_func():
        """退出程序时序列化各对象数据"""
        Serialize.dump(settings.SCHOOL_DB, settings.SCHOOLS_DATA)
        Serialize.dump(settings.COURSE_DB, settings.COURSES_DATA)
        Serialize.dump(settings.TEACHER_DB, settings.TEACHERS_DATA)
        Serialize.dump(settings.CLASSES_DB, settings.CLASSES_DATA)
        Serialize.dump(settings.ACCOUNT_DB, settings.ACCOUNTS_DATA)
        Serialize.dump(settings.STUDENT_DB, settings.STUDENTS_DATA)
        settings.EXIT_FLAG = True