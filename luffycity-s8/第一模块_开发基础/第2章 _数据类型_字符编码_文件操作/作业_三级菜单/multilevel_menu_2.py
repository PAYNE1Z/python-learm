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

current_layer = menu
layers = []
exit_flag = False

while not exit_flag:
    print('MENU'.center(30, '='))
    for k in current_layer:
        print(k)
    choice = input('请选择以上选项输入[退出：q; 返回上层: b]>>:').strip()
    if choice in current_layer:
        layers.append(current_layer)
        current_layer = current_layer[choice]
    elif choice == 'b':
        if layers:
            current_layer = layers.pop()
        else:
            print('已经是最顶层了')
    elif choice == 'q':
        exit_flag = True
        print('bey.')
    else:
        print('没有此选项')