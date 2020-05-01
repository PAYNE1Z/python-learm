#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/24
# Location: DongGuang
# Desc:     登录认证


import time
from conf import settings
from modules import md5
from modules import serialization
from modules import check_user_exist
from modules.logger import log


def check_user_status(user, user_data):
    """
    验证帐号状态
    :param user: 用户名
    :param user_data: 用户数据
    :return: True of False  0为正常;1为锁定
    """
    if user_data['status'] == 0:
        return True
    else:
        log(log_type, 'both').error('[{}]该帐号已被锁定'.format(user))
        return False


def is_expire(user, user_data):
    """
    验证帐号是否过期
    :param user: 用户名
    :param user_data: 用户数据
    :return: 过期True of 未过期False
    """
    expire_date = user_data['expire_date']
    expire_strptime = time.mktime(time.strptime(expire_date, '%Y-%m-%d'))
    if expire_strptime > time.mktime(time.localtime()):
        return False
    else:
        log(log_type, 'both').warning('[{}]帐号已过期'.format(user))
        return True


def password_auth(user, user_data, user_db):
    """
    密码验证与重试
    :param user: 用户名
    :param user_data: 用户数据
    :param user_db: 用户数据文件
    """
    max_retry = settings.PASSWORD_MAX_RETRY
    p = 0
    while p < max_retry:  # 密码重试
        u_pass = input('Password>>>: ')
        if md5.make_md5(u_pass) == user_data['password']:
            log(log_type, 'file').info('[{}] 密码验证成功'.format(user))
            return True
        else:
            log(log_type, 'both').warning('密码错误，请重试')
        p += 1
    else:
        log(log_type, 'both').error('重试次数过多，帐号已被锁定')
        user_data['status'] = 1
        # 保存所做修改
        serialization.dump_account(user_data, user_db)
        log(log_type, 'file').info('[{}]帐号状态已变更：[{}]'.format(user, user_data['status']))
        exit(0)


def auth(user_type):
    """
    接收装饰器参数
    :param user_type: [user|admin] 验证类型
    """
    # 接收执行函数方法
    def auth_func(func):

        # 认证函数
        def wrapper():
            global log_type
            log_type = 'login'
            print('请输入用户帐号与密码') if user_type == 'user' else print('请输入管理员帐号与密码')
            while True:
                user = input('User>>>: ')
                if check_user_exist.is_exist(user, 'check', user_type):  # 检测帐号是否存在
                    user_db = check_user_exist.is_exist(user, 'get', user_type)  # 获取帐号文件路径
                    user_data = serialization.load_account(user_db)
                    if check_user_status(user, user_data) and not is_expire(user, user_data) \
                            and password_auth(user, user_data, user_db):  # 检测帐号是否被锁定、过期; 密码是否正常
                        log(log_type, 'both').info('[{}] 欢迎光临'.format(user))
                        return func(user_data, user_db)
                else:
                    log(log_type, 'both').warning('[{}]帐号不存在'.format(user))
                    return 0
        return wrapper
    return auth_func