#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/20
# Location: DongGuang
# Desc:     re模块练习 使用正则实现一个计算器功能


"""
需求：
    开发一个简单的python计算器，实现加减乘除及拓号优先级解析
    用户输入 1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )
    等类似公式后，必须自己解析里面的(),+,-,*,/符号和公式
    (不能调用eval等类似功能偷懒实现)，
    运算后得出结果，结果必须与真实的计算器所得出的结果一致
"""

import re


def multiply_operation(multiply_eq):
    """
    乘法运算
    :param multiply_eq: 乘法公式
    :return: 运算结果
    """
    multiply_eq = re.sub('\(|\)', '', multiply_eq)
    print(multiply_eq)
    ret = re.search('(\d+)\*(\d+)', multiply_eq)

    if ret:
        print(ret.groups())


def divide_operation(divide_eq):
    """
    除法运算
    :param divide_eq: 除法公式
    :return: 运算结果
    """
    # divide_eq = re.sub('\(|\)', '', divide_eq)
    print("divide:", divide_eq)
    pattern = '([^\d-]*-?\d+)/([^/\+\*-0-9]?[-]?\d+)'
    div_pattern = re.compile(pattern)
    ret = div_pattern.search(divide_eq)
    print("###ret:", ret)
    if ret:
        print("groups:", ret.groups())
        div_ret = int(ret.groups()[0]) / int(ret.groups()[1])

        # if re.match(ret.groups()[0], divide_eq):
        #     div_ret = int(ret.groups()[0]) / int(ret.groups()[1])
        # else:
        #     div_ret = abs(int(ret.groups()[0])) / int(ret.groups()[1])
        print(div_ret)
        divide_eq = re.sub(pattern, str(div_ret), divide_eq)
        print("XXX:", divide_eq)
        divide_operation(str(div_ret))  #
    else:
        return divide_eq


def add_operation(add_eq):
    """
    加法运算
    :param add_eq: 加法公式
    :return: 运算结果
    """
    add_eq = re.sub('\(|\)', '', add_eq)
    print(add_eq)
    ret = re.search('([-]?\d+)\+(\d+)', add_eq)
    if ret:
        print(ret.groups())
        if re.match(ret.groups()[0], add_eq):
            add_ret = int(ret.groups()[0]) / int(ret.groups()[1])
            print(add_ret)
        else:
            add_ret = abs(int(ret.groups()[0])) / int(ret.groups()[1])
            print(add_ret)
        divide_operation(add_eq)
    else:
        pass


def subtract_operation(subtract_eq):
    """
    减法运算
    :param subtract_eq: 减法公式
    :return: 运算结果
    """
    subtract_eq = re.sub('\(|\)', '', subtract_eq)
    print(subtract_eq)
    ret = re.search('([-]?\d+)\+(\d+)', subtract_eq)
    if ret:
        print(ret.groups())
        if re.match(ret.groups()[0], subtract_eq):
            sub_ret = int(ret.groups()[0]) / int(ret.groups()[1])
            print(sub_ret)
        else:
            sub_ret = abs(int(ret.groups()[0])) / int(ret.groups()[1])
            print(sub_ret)
        divide_operation(subtract_eq)
    else:
        pass


def calculate(eq):
    """
    计算算式的结果
    :param eq: 算式
    :return: 公式计算结果
    """
    eq = re.sub('\s+', '', eq)
    bracket_pattern = re.compile('\(([^()]+)\)')
    print(eq)
    ret = bracket_pattern.search(eq)
    print(ret.group())

    if ret:
        ret = re.sub('\(|\)', '', ret.group())
        if re.search('/', ret):
            div_ret = divide_operation(ret)
            print("####:", div_ret)
        elif re.search('\*', ret):
            multiply_operation(ret)
        elif re.search('\+', ret):
            add_operation(ret)
        elif re.search('-', ret):
            subtract_operation(ret)
    else:
        pass


equation = '1 - 2 * ( (60-30 +(4*5-40/-5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )'

calculate(equation)

