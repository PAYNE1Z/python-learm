#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/20
# Location: DongGuang
# Desc:     登录认证


from modules.new_input import new_input
from conf import settings


def auth(user_type):
    """
    登录认证
    :param user_type: 认证用户类型
    """
    count = 0
    while count < 3:
        print('请输入[{}]类型帐号密码'.format(user_type))
        user = new_input('User>>>: ')
        pwd = new_input('Password>>>: ')
        if user in settings.ACCOUNTS_DATA:
            if settings.ACCOUNTS_DATA[user]['pwd'] == pwd and settings.ACCOUNTS_DATA[user]['type'] == user_type:
                print('[{}]:[{}]登录成功'.format(settings.ACCOUNTS_DATA[user]['type'], user))
                auth_info = {'type': settings.ACCOUNTS_DATA[user]['type'], 'name': user, 'ret': True}
                break
            else:
                print('密码不正确或[{}]帐号不属于[{}]类型'.format(user, user_type))
                auth_info = {'name': user, 'ret': False}
        else:
            print('帐号不存在')
            auth_info = {'name': user, 'ret': False}
        count += 1
    return auth_info