#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/5
# Location: DongGuang
# Desc:     do the right thing


"""
练习：定义MySQL类

要求：
    1.对象有id、host、port三个属性
    2.定义工具create_id，在实例化时为每个对象随机生成id，保证id唯一
    3.提供两种实例化方式，方式一：用户传入host和port 方式二：从配置文件中读取host和port进行实例化
    4.为对象定制方法，save和get_obj_by_id，save能自动将对象序列化到文件中，
    文件路径为配置文件中DB_PATH,文件名为id号，保存之前验证对象是否已经存在，若存在则抛出异常
    get_obj_by_id方法用来从文件中反序列化出对象
"""

import settings
import hashlib
import pickle
import os


class MySQL:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.id = MySQL.create_id(self)  # 通过类自己调用非绑定方法创建ID
        self.obj_file = '{}/{}'.format(settings.DB_PATH, self.id)

    @classmethod
    def from_conf(cls):  # 从配置文件实例化对象（调用者的类通过cls传入）
        obj = cls(settings.DB_HOST, settings.DB_PORT)
        return obj

    @staticmethod
    def create_id(obj):  # 创建对象ID号 (host+port的md5值)
        m = hashlib.md5((str(obj.host) + str(obj.port)).encode('utf8'))
        return m.hexdigest()

    def save(self):  # 序列化对象到文件，文件名为对象的ID号
        if not os.path.isfile(self.obj_file):
            with open(self.obj_file, 'wb') as f:
                pickle.dump(self, f)
        else:
            print('{} ID对象已经存在'.format(os.path.basename(self.obj_file)))

    def get_obj_by_id(self):  # 从序列化文件中获取对象
        try:
            with open(self.obj_file, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print('{} ID对象不存在'.format(os.path.basename(self.obj_file)))


my1 = MySQL('localhost', 13306)  # MySQL(my1,'localhost',13306) 通过用户传入host,port实例化对象
my2 = MySQL.from_conf()    # MySQL.from_conf(MySQL) 通过类绑定方法自动从配置文件中获取host,port来实例化对象

# my1.save()
# my2.save()
my1_1 = my1.get_obj_by_id()
my2_2 = my2.get_obj_by_id()
print('my1_1 obj:', my1_1.__dict__)
print('my2_2 obj:', my2_2.__dict__)

