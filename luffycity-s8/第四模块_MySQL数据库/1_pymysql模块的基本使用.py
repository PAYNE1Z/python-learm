#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/12
# Location: DongGuang
# Desc:     do the right thing


import pymysql

# 1、建立连接
conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='123456',
    db='db4',
    charset='utf8'
)


# 2、拿到游标
cursor = conn.cursor()


# 3、执行SQL获取结果
sql = 'select * from employee where name="alex"'
print('SQL: ', sql)
rows = cursor.execute(sql)

# 这里返回的是受影响的记录条数，如果为0，表示没有匹配记录
# MySQL命令行： 1 rows in set (0.01 sec)
print('RET: ', rows)

# 4、关闭游标与连接
cursor.close()
conn.close()