#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/15
# Location: DongGuang
# Desc:     time模块


import time

# 明文时间格式转时间戳
time.mktime(time.strptime('2018 04-25-13', '%Y %m-%d-%H'))
# 1524632400.0


# 时间戳转换成明文时间格式
time.strftime('%Y %m %d %H:%M:%S', time.localtime())
# '2019 05 15 16:51:56'
time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(15344342))
# '1970-06-27 22:19:02'

"""
转换流程
    '2018-11-10 18:08:08' time.strptime ->   [time.struct_time]   ->   time.mktime 1541844488.0 
    1541844488.0 time.localtime/time.gmtime ->  [time.struct_time]  ->   time.strftime '2018-11-10 18:08:08'
"""