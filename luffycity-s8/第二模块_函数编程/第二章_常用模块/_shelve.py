#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/16
# Location: DongGuang
# Desc:     序列化模块 shelve



"""
shelve 模块是一个简单的k,v将内存数据通过文件持久化的模块，
可以持久化任何pickle可支持的python数据格式
shelve 其实就是内部就是调用的pickle，所以其它序列化的数据也只有python能识别使用
"""

import shelve

# 序列化
names = ['jack', 'robin', 'pony']
info = {'name': 'alex', 'age': 22, 'phone': 18666888866}

with shelve.open('shelve_test') as f:  # 打开文件
    # 会产生三个文件: .bak .dat .dir
    f['names_list'] = names      # 持久化
    f['info_dict'] = info


# 反序列化
with shelve.open('shelve_test') as f:
    print(f['names_list'])      # 取数据
    print(f['names_list'][2])
    print(f['info_dict']['phone'])

    f['top'] = [1,2,3,4,5]  # 新增数据

    # 修改数据(只能修改最外层的key对应的数据，如果值是一个列表或字典之类的数据集合，不能只修改其中的某个元素)
    f['names'] = ['Jack', 'Robin', 'Pony']  # ok
    f['names'][1] = 'Robin Li'  # 无法修改
    print(f['names'])

    # 删除数据
    del f['name']
