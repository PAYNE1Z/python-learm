#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/4
# Location: DongGuang
# Desc:     do the right thing



"""
绑定方法:
    绑定给对象的方法（没有被任何装饰器装饰的方法）
    绑定给类的方法（用classmethod装饰器装饰的方法）
        classmehtod是给类用的，即绑定到类，类在使用时会将类本身当做参数传给类方法的第一个参数（即便是对象来调用也会将类当作第一个参数传入），
        python为我们内置了函数classmethod来把类中的函数定义成类方法

非绑定方法:
    在类内部用staticmethod装饰的函数即非绑定方法，就是普通函数
    statimethod不与类或对象绑定，谁都可以调用，没有自动传值效果
"""

import hashlib
import time

HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
PASSWORD = '123456'


class MySQL:
    def __init__(self, host, port, user, pwd):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd

    def connect(self):  # 对象绑定方法，没有被任何装装饰器装饰过的方法
        # 哪个对象来调用,就将哪个对象当做第一个参数传入
        print('{} connect to {}'.format(self.user, self.host))

    @classmethod
    def exec(cls):
        # 类绑定方法，对象与类都可以调用，但默认传的第一个参数仍然是类
        # 哪个类来调用,就将哪个类当做第一个参数传入; 官方将cls做为传入类的变量名
        print('is exec', cls)

    @staticmethod
    def create_id(string):  # 非绑定方法，就是一个普通工具，有参数的话需要在调用时传入
        # statimethod不与类或对象绑定，谁都可以调用，没有自动传值效果
        m = hashlib.md5(str(string).encode('utf8'))
        return m.hexdigest()



# 绑定到类, 通过classmethod装饰
# 可以看到不管是类来调用还是对象来调用都变成了bound method了，不再是个普通的function
# 类调用
print(MySQL.exec)  # <bound method MySQL.exec of <class '__main__.MySQL'>>
MySQL.exec()  # is exec <class '__main__.MySQL'>
mysql = MySQL(HOST, PORT, USER, PASSWORD)
# 对象调用
print(mysql.exec)  # <bound method MySQL.exec of <class '__main__.MySQL'>>
mysql.exec()  # is exec <class '__main__.MySQL'>



# 绑定到对象
# 对象调用，可以看到当对象来调用时方法是bound method; 并且会自动的把对象本身当成第一个参数传给类
print(mysql.connect)  # <bound method MySQL.connect of <__main__.MySQL object at 0x000001EE77494550>>
mysql.connect()  # root connect to 127.0.0.1
# 类调用，当类来调用时方法是个普通的function,并且需要手动将对象当做第一个参数传入
print(MySQL.connect)  # <function MySQL.connect at 0x00000213B7DF37B8>
MySQL.connect(mysql)  # root connect to 127.0.0.1



# 非绑定方法 通过staticmethod装饰（就是一个普通函数），
# 可以看到不管是对象还是类调用，都是变通的function, 并不需要再将调用者当成参数传入, 只需要传入方法本身所需要的参数
# 对象来调用
print(mysql.create_id)  # <function MySQL.create_id at 0x000001C0144839D8>
# 类来调用
print(MySQL.create_id)  # <function MySQL.create_id at 0x00000231561839D8>
md5 = mysql.create_id(time.time())  # 586d2bcbfea1e3868953f54c298d5803
md52 = MySQL.create_id(time.time())  # 586d2bcbfea1e3868953f54c298d5803
print(md5, md52)