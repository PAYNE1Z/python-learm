#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/4/28
# Location: DongGuang
# Desc:     do the right thing

import copy


name = [['pony', 'dong'], 'jack', 'robin']
print("########### name: %s\n" % name)

name1 = name
print("###>>> name1 = name")
print("===============================")
print("修改前列表内存地址：", id(name), id(name1))
print("修改前列表索引1的值的内存地址：", id(name[1]), id(name1[1]))
print("> 将name中索引1的值改为 dong")
name[1] = 'dong'
print("修改后列表内存地址：", id(name), id(name1))
print("修改后列表索引1的值的内存地址：", id(name[1]), id(name1[1]), "\n")


name2 = name.copy()
print("###>>> name2 = name.copy()")
print("===============================")
print("修改前列表内存地址：", id(name), id(name2))
print("修改前列表索引1的值的内存地址：", id(name[1]), id(name2[1]))
print("> 将name中索引1的值改为 dong")
name[1] = 'lei'
print("修改后列表内存地址：", id(name), id(name2))
print("修改后列表索引1的值的内存地址：", id(name[1]), id(name2[1]))
print("> 将name中子列表中索引1的值改为 long")
name[0][1] = 'long'
print("修改后列表内存地址：", id(name), id(name2))
print("修改后列表索引1的值的内存地址：", id(name[0][1]), id(name2[0][1]), "\n")


name3 = copy.deepcopy(name)
print("###>>> name3 = copy.deepcopy(name)")
print("===============================")
print("修改前列表内存地址：", id(name), id(name3))
print("修改前列表索引1的值的内存地址：", id(name[1]), id(name3[1]))
print("> 将name中索引1的值改为 dong")
name[1] = 'zhang'
print("修改后列表内存地址：", id(name), id(name3))
print("修改后列表索引1的值的内存地址：", id(name[1]), id(name3[1]))
print("> 将name中子列表中索引1的值改为 long")
name[0][1] = 'cheng'
print("修改后列表内存地址：", id(name), id(name3))
print("修改后列表索引1的值的内存地址：", id(name[0][1]), id(name3[0][1]), "\n")

