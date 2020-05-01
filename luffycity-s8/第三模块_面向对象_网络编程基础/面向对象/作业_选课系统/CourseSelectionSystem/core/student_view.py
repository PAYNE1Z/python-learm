#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/30
# Location: DongGuang
# Desc:     学生视图


from conf import settings
from core.manager_view import ManagerView
from modules.is_number import is_number
from core.school import *


class StudentView(Student, ManagerView):
    """学员类：
    绑定班级(每个学员只能绑定一个班级,绑定了班级就是选定了课程)
    课程是与班级绑定的
    """
    func_list = [
        ('学员注册', 'registration'),
        ('选择班级', 'student_choice_classes'),
        ('缴费', 'pay_tuition'),
        ('查看当前学员信息', 'show_student_info'),
        ('退出', 'exit_func')
    ]

    def __init__(self, name):
        self.name = name

    def registration(self):
        """学员注册"""
        sex_list = ['male', 'female']
        print('当前学员姓名为: [{}]'.format(self.name))
        if not is_exist(self.name, settings.STUDENTS_DATA):
            stu_age = is_number(new_input('请输入年龄>>>: '))
            if stu_age:
                stu_sex = new_input('请输入学员性别[{}]>>>: '.format('|'.join(sex_list)))
                if stu_sex in sex_list:
                    stu_obj = Student(self.name, stu_age, stu_sex)
                    settings.STUDENTS_DATA[self.name] = stu_obj
                    print('[{}]学员注册成功'.format(self.name))
                else:
                    print('无效的性别选项')

    def student_choice_classes(self):
        """学员选择班级"""
        print('当前要选择班级的学员为: [{}]'.format(self.name))
        # 一个学员只能绑定一个班
        stu_obj = settings.STUDENTS_DATA.get(self.name)
        if stu_obj:
            classes_obj = super().select_obj(settings.CLASSES_DATA, 'classes')
            if classes_obj:
                if stu_obj.classes_name is None:
                    school_obj = settings.SCHOOLS_DATA[classes_obj.school_addr]  # 获取班级所在校区对象
                    stu_obj.classes_name = classes_obj.name          # 将班级绑定到学员
                    stu_obj.course_name = classes_obj.course_name    # 将班级课程绑定到学员
                    stu_obj.teacher_name = classes_obj.teacher_name  # 将班级老师绑定到学员
                    classes_obj.students.append(self.name)         # 将学员加班班级学员列表
                    school_obj.students.append(self.name)          # 将学员加到校区学员列表
                    settings.STUDENTS_DATA[self.name] = stu_obj            # 更新学生对象数据
                    settings.CLASSES_DATA[classes_obj.name] = classes_obj  # 更新班级对象数据
                    settings.SCHOOLS_DATA[school_obj.addr] = school_obj    # 更新学校对象数据
                    print('[{}]学员已加入班级:[{}]'.format(self.name, classes_obj.name))
                else:
                    print('[{}]学员已在班级[{}]'.format(self.name, stu_obj.classes_name))

    def pay_tuition(self):
        """交学费"""
        print('当前要缴费的学员为: [{}]'.format(self.name))
        stu_obj = settings.STUDENTS_DATA.get(self.name)
        if stu_obj:
            if stu_obj.course_name:
                print('班级: {}; 课程: {}; 课程费用: {}'.format(
                    stu_obj.classes_name, stu_obj.course_name, settings.COURSES_DATA.get(stu_obj.course_name).price))
                if not stu_obj.pay_status:
                    choice = new_input('确认缴费请按[y|Y]>>>: ')
                    if choice.upper() == 'Y':
                        print('缴费成功')
                        stu_obj.pay_status = True  # 缴费后将缴费状态改为 True
                        settings.STUDENTS_DATA[self.name] = stu_obj  # 更新学员数据字典
                    else:
                        print('选项错误,缴费未成功')
                else:
                    print('该学员已经交过学费了')
            else:
                print('该学员还没有选择班级课程')

    def show_student_info(self):
        """学生自己查看自己信息"""
        stu_obj = settings.STUDENTS_DATA.get(self.name)
        if stu_obj:
            print('STUDENT INFO'.center(30, '+'))
            print(stu_obj)
            print(''.center(30, '+'))

