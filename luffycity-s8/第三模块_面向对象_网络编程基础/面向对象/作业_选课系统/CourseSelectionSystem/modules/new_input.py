#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/28
# Location: DongGuang
# Desc:     自定义input函数，默认strip()处理用户输入


def new_input(msg):
    return input(msg).strip()