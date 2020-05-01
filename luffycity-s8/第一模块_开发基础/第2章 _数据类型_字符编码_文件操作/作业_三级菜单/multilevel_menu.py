#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/4/30
# Location: DongGuang
# Desc:     第一模块 第二章作业<多级菜单>

"""
需求：
1. 可依次选择进入各子菜单
2. 可从任意一层往回退到上一层
3. 可从任意一层退出程序
"""

menu = {
    '北京': {
        '海淀': {
            '五道口': {
                'soho': {},
                '网易': {},
                'google': {}
            },
            '中关村': {
                '爱奇艺': {},
                '汽车之家': {},
                'youku': {},
            },
            '上地': {
                '百度': {},
            },
        },
        '昌平': {
            '沙河':{
                '老男孩': {},
                '北航': {},
            },
            '天通苑': {},
            '回龙观': {},
        },
        '朝阳': {},
        '东城': {},
    },
    '上海': {
        '闵行': {
            "人民广场": {
                '炸鸡店':{}
            }
        },
        '闸北': {
            '火车战': {
                '携程': {}
            }
        },
        '浦东': {},
    },
    '山东': {}
}

cache_list = []  # 存储层级历史记录

while True:
    next_menu = menu
    for i in cache_list:
        next_menu = next_menu[i]  # 以用户输入key生成新的下层字典
    print("中国城市列表".center(30, '='))
    for key in next_menu:  # 打印用户选择层级下的所有key
        print(key)
    choice = input("\033[34m\n>>>请输入查找的地名【如要退出请按：q ; 返回上级菜单请按：b】 >>: \033[0m")
    if choice == 'q':  # 退出
        exit("\033[34m欢迎您下次使用！再见\033[0m")
    elif choice == 'b':  # 返回上层时在列表中删除当前层级
        if len(cache_list) > 0:
            cache_list.pop()multilevel_menu.py
        else:
            print("\033[32m这已经是最上层了\033[0m")
    elif next_menu.get(choice):  # 进入下层时将当前层级存入列表
        cache_list.append(choice)
    else:
        print("\033[1;31m[%s]暂无下层信息或没有此选项，请重新选择\033[0m" % choice)