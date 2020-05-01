#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/9
# Location: DongGuang
# Desc:     经过strip()方法处理的input函数


def strip_input(msg):
    """给input方法封装一层strip
    """
    return input(msg).strip()

