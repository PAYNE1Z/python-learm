#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/28
# Location: DongGuang
# Desc:     检测字符串是否是数字


def is_number(in_str):
    """检测字符串是否是数字并返回int类型"""
    try:
        return int(in_str)
    except ValueError:
        print('请输入数字类型')
        return False
