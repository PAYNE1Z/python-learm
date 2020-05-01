#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/12
# Location: DongGuang
# Desc:     do the right thing


import pymysql


user = input('User>>: ').strip()
password = input('Password>>: ').strip()


conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='123456',
    db='db4',
    charset='utf8'
)

cursor = conn.cursor()


# sql = f'select * from user where name="{user}" and password=md5("{password}");'   # 自己拼接
sql = 'select * from user where name=%s and password=md5(%s);'     # execute拼接（注意不要给%s加引号）
print('SQL: ', sql)

# 当我们自己拼接sql语句时会出现严重的安全问题

# 如：客户输入用户名时输入: jack" -- password abc 我们看到的sql语句是这样的：
# SQL:  select * from user where name="jack" -- password abc and password=md5("abc");
# -- 双减号在sql中是注释，所有--后面的都不会被执行，那么用户只用用户名就能成功登录

# 当客户输入用户名时输入：xxxx" or 1=1 -- abc 我们看到的sql语句是这样的：
# SQL:  select * from user where name="xxxx" or 1=1 -- abc" and password=md5("abc");
# 帐号密码都错了的情况下，都能登录成功

# 所以SQL语句的拼接我们交给pymysql模块的execute处理
rows = cursor.execute(sql, (user, password))  # 把帐号密码以无袓的形式传给execute

print('登录成功') if rows else print('登录失败')

cursor.close()
conn.close()

