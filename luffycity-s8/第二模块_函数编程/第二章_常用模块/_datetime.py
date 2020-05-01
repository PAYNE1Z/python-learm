#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/15
# Location: DongGuang
# Desc:     datetime 模块


import datetime

# 1、返回当前日期
d = datetime.datetime.now()
print(d)  # 2019-05-15 17:29:50.790062
print(d.timestamp())  # 1557912697.453118
print(d.today())      # 2019-05-15 17:31:37.453118
print(d.month)        # 5
print(d.year)         # 2019
print(d.timetuple())
# time.struct_time(tm_year=2019, tm_mon=5, tm_mday=15, tm_hour=17, tm_min=31, tm_sec=37, tm_wday=2, tm_yday=135, tm_isdst=-1)


# 2、将时间戳转换为日期
print(datetime.date.fromtimestamp(1402434))
# 1970-01-17


# 3、时间运算
d = datetime.datetime.now()
print(datetime.timedelta(4) + d)           # 当前时间加4天(往后推四天)
print(datetime.timedelta(days=4) + d)
print(datetime.timedelta(hours=4) + d)     # 当前时间加4小时(往后推四小时)
print(datetime.timedelta(minutes=20) + d)  # 当前时间加20分钟(往后推20分钟)
print(datetime.timedelta(seconds=10) + d)  # 当前时间加10秒(往后推10秒)


# 4、时间替换
d = datetime.datetime.now()
new_d = d.replace(year=2017,month=9,day=25)   # 把当前时间替换为 2017-09-25
print(new_d)
