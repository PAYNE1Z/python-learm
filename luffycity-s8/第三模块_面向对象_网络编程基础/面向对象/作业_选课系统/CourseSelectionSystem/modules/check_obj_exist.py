#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/1
# Location: DongGuang
# Desc:     判断一个对象是否存在


def is_exist(obj, data, flag='not'):
    """
    检测某个对象是否存在
    :param obj: 要检测的对象
    :param data: 对象数据集
    :param flag: 检测标志: not:存在 in:不存在  根据这个标志打印存在或不存在
    :return True or False
    """
    check_flag = False
    if obj in data:
        check_flag = True
    if check_flag and flag == 'not':
        print('[{}]已存在'.format(obj))
    if not check_flag and flag == 'in':
        print('[{}]不存在'.format(obj))
    return check_flag



