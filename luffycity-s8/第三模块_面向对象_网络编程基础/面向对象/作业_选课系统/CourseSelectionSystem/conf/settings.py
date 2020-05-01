#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/10
# Location: DongGuang
# Desc:     全局配置


import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from modules.serialization import Serialize

# 数据存档目录
DB_DIR = os.path.join(BASE_DIR, 'data', 'db')

# 登录帐户信息文件
ACCOUNT_DB = os.path.join(DB_DIR, 'account.pk')

# 学生信息存档文件
STUDENT_DB = os.path.join(DB_DIR, 'student.pk')

# 老师信息存档文件
TEACHER_DB = os.path.join(DB_DIR, 'teacher.pk')

# 班级信息存档文件
CLASSES_DB = os.path.join(DB_DIR, 'classes.pk')

# 学校信息存档文件
SCHOOL_DB = os.path.join(DB_DIR, 'school.pk')

# 课程信息存档文件
COURSE_DB = os.path.join(DB_DIR, 'courses.pk')

# 用户类型列表
USER_TYPE_LIST = ['Manager', 'Teacher', 'Student']

# 初始化加载各对象数据
# 学校
SCHOOLS_DATA = Serialize.load(SCHOOL_DB)
# 课程
COURSES_DATA = Serialize.load(COURSE_DB)
# 老师
TEACHERS_DATA = Serialize.load(TEACHER_DB)
# 班级
CLASSES_DATA = Serialize.load(CLASSES_DB)
# 学生
STUDENTS_DATA = Serialize.load(STUDENT_DB)
# 登录帐户
ACCOUNTS_DATA = Serialize.load(ACCOUNT_DB)
if not ACCOUNTS_DATA:  # 初始化一个管理帐号
    ACCOUNTS_DATA = {"admin": {"pwd": "admin", "type": "Manager"}}
    Serialize.dump(ACCOUNT_DB, ACCOUNTS_DATA)

# 循环标志
EXIT_FLAG = False