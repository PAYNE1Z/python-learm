#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/12
# Location: DongGuang
# Desc:     do the right thing


import pymysql


conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='db4', charset='utf8')
cursor = conn.cursor()
# cursor = conn.cursor(pymysql.cursors.DictCursor)  # fetch的结果将以字典形式呈现

# 增， 删， 改
sql1 = 'insert into user (name, password) values ("root", "abceff");'
res = cursor.execute(sql1)
print('res1:', res)

sql2 = 'insert into user (name, password) values (%s, %s);'
res = cursor.execute(sql2, ('joshua', 'abcccc'))
print(cursor.lastrowid)  # 查看自增ID的下一位是多少(当前最后一位ID+1), 只能在insert语句后才能用
print('res2:', res)

sql3 = 'insert into user (name, password) values (%s, %s);'
user_info_lst = [('user1', '123'), ('user2', '123'), ('user3', '123')]
res = cursor.executemany(sql3, user_info_lst)   # 插入多条数据
print('res3:', res)

sql4 = 'delete from user where name="joshua";'
res = cursor.execute(sql4)
print('res4:', res)

sql5 = 'update user set password=md5(password);'
res = cursor.execute(sql5)
print('res5:', res)

# commit后这些记录才会记录到数据库中
conn.commit()

# 查
sql6 = 'select * from user;'
rows = cursor.execute(sql6)  # 执行sql语句，返回sql影响成功的行数rows,将结果放入一个集合，等待被查询
res1 = cursor.fetchone()    # 取1条查询到的记录

cursor.scroll(2, mode='absolute')   # 从绝对路径移动，从头跳过2条数据
res2 = cursor.fetchmany(2)  # 取2条查询到的记录

cursor.scroll(1, mode='relative')   # 从绝对路径移动，从当前位置跳过1条数据
res3 = cursor.fetchall()    # 取所有查询到的记录

print('res1:', res1)
print('res2:', res2)
print('res3:', res3)
print(f'{rows} rows in set (0.00 sec)')


cursor.close()
conn.close()