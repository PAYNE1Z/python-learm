#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/10
# Location: DongGuang
# Desc:     程序主入口


import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from conf import settings
from modules.login import auth
from modules.is_number import is_number
from modules.new_input import new_input
from core.school import School


class Views:
    """视图"""
    def __init__(self, user_type):
        self.user_type = user_type

    def views_dist(self):
        """视图分发"""
        auth_info = auth(self.user_type)
        if auth_info['ret']:
            cls_str = '{}View'.format(auth_info['type'])
            if cls_str in globals():
                cls_obj = globals()[cls_str](auth_info['name'])  # 将登录用户名传递给个各视图函数，以便相关视图控制权限
            while not settings.EXIT_FLAG:
                print(' {} '.format(self.user_type).upper().center(30, '='))
                for idx, item in enumerate(cls_obj.func_list, 1):
                    print('{}. {}'.format(idx, item[0]))
                choice = is_number(new_input('请输入功能选项>>>: '))
                if choice:
                    func_str = cls_obj.func_list[choice - 1][1]  # 取功能列表中的功能字符串(取值要从0开始取)
                    if hasattr(cls_obj, func_str):  # 判断obj中是否有func_str方法
                        getattr(cls_obj, func_str)()  # 获取方法对象并执行
                    else:
                        print('{}方法不存在'.format(func_str))


def main():
    """入口"""
    func_list = [
        ('管理员视图', 'Manager'),
        ('老师视图', 'Teacher'),
        ('学生视图', 'Student'),
        ('退出', None)
    ]
    while True:
        print(' {} '.format(School.school_name).center(30, '='))
        for num, item in enumerate(func_list, 1):
            print('{}. {}'.format(num, item[0]))
        choice = is_number(input('请输入功能编号>>: '))
        if choice in [1, 2, 3]:
            settings.EXIT_FLAG = False
            views = Views(func_list[choice-1][1])
            views.views_dist()
        elif choice == 4:
            exit('Bye!!!')
        else:
            print('无效的选项')


if __name__ == "__main__":
    main()
