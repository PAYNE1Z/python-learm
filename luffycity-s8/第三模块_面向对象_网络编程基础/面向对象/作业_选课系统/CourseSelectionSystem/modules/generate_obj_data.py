#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/30
# Location: DongGuang
# Desc:     生成某个对象中某个对象的数据字典


def generate(source_data, filter_name):
    """
    通过指定对象名称从所有该类型对象的数控字典过滤出所需的数据
    :param source_data: 该类型所有对象数据字典
    :param filter_name: 要提取的对象属性与名称 eg: ['alex', 'egon',...]
    :return: 指定对象数据字典 eg: {'obj_name': 'obj', ...}
    """
    new_data = {}
    for obj_name in source_data:
        if obj_name in filter_name:
            new_data[obj_name] = source_data[obj_name]
    return new_data