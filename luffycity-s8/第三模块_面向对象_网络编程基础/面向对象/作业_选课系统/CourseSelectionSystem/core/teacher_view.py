#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/30
# Location: DongGuang
# Desc:     老师视图


from conf import settings
from core.manager_view import ManagerView
from modules.is_number import is_number
from modules.generate_obj_data import generate
from core.school import *


class TeacherView(Teacher, ManagerView):
    """老师类：绑定校区(只能绑定一个校区)，可以选择多个班级授课(只能选择所在校区的班级)"""
    func_list = [
        ('选择上课班级', 'teacher_choice_classes'),
        ('查看班级学员', 'show_classes_students'),
        ('修改学员成绩', 'update_student_score'),
        ('查看当前老师信息', 'show_teacher_info'),
        ('退出', 'exit_func')
    ]

    def __init__(self, name):
        self.name = name

    def teacher_choice_classes(self):
        """选择上课班级"""
        print('当前要操作的老师为: [{}]'.format(self.name))
        teacher_obj = settings.TEACHERS_DATA.get(self.name)
        if teacher_obj:
            # 打印老师所在校区的班级
            classes_obj = super().select_obj(
                generate(settings.CLASSES_DATA, settings.SCHOOLS_DATA[teacher_obj.school_addr].classes),'classes')
            if classes_obj:
                if not is_exist(classes_obj.name, teacher_obj.classes):
                    teacher_obj.classes.append(classes_obj.name)  # 班级绑定到老师
                    classes_obj.teacher_name = self.name          # 将老师加入班级
                    settings.CLASSES_DATA[classes_obj.name] = classes_obj  # 更新班级数据字典
                    settings.TEACHERS_DATA[self.name] = teacher_obj        # 更新老师数据字典
                    print('[{}]老师选择班级[{}]成功'.format(self.name, classes_obj.name))

    def show_classes_students(self):
        """查看班级学员列表"""
        print('当前老帅为: [{}]'.format(self.name))
        teacher_obj = settings.TEACHERS_DATA.get(self.name)
        if teacher_obj:
            # 老师管理的班级
            classes_obj = super().select_obj(generate(settings.CLASSES_DATA, teacher_obj.classes), 'classes')
            if classes_obj:
                if is_exist(classes_obj.name, teacher_obj.classes, 'in'):
                    print('所选班级的学员信息'.center(30, '+'))
                    super().show_obj(
                        generate(settings.STUDENTS_DATA, settings.CLASSES_DATA[classes_obj.name].students))

    def update_student_score(self):
        """修改学员成绩"""
        print('当前老帅为: [{}]'.format(self.name))
        teacher_obj = settings.TEACHERS_DATA.get(self.name)
        if teacher_obj:
            # 老师管理的班级
            classes_obj = super().select_obj(generate(settings.CLASSES_DATA, teacher_obj.classes), 'classes')
            if classes_obj:
                # 班级必须是当前老师管理的班级
                if is_exist(classes_obj.name, settings.TEACHERS_DATA.get(self.name).classes, 'in'):
                    # 打印所选班级的学员
                    student_obj = super().select_obj(
                        generate(settings.STUDENTS_DATA, settings.CLASSES_DATA.get(classes_obj.name).students), 'students')
                    if student_obj:
                        # 学员必须在当前老师管理班级中
                        if is_exist(student_obj.name, settings.CLASSES_DATA.get(classes_obj.name).students, 'in'):
                            new_score = is_number(new_input('学员[{}]课程当前分数为:[{}]\n请输入新的分数>>>: '.format(
                                student_obj.name, student_obj.score)))
                            if new_score:
                                student_obj.score = new_score
                                settings.STUDENTS_DATA[self.name] = student_obj   # 更新学员数据字典
                                print('[{}]学员[{}]成绩修改成功'.format(student_obj.name, student_obj.course_name))

    def show_teacher_info(self):
        """老师自己查看自己信息"""
        teh_obj = settings.TEACHERS_DATA.get(self.name)
        if teh_obj:
            print('TEACHER INFO'.center(30, '+'))
            print(teh_obj)
            print(''.center(30, '+'))
