#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/30
# Location: DongGuang
# Desc:     创建各对象登录帐号


from conf import settings
from modules.new_input import new_input


def make_account(user_name=None, user_type=None):
    """
    创建登录帐号
    :param user_name: 帐号名称
    :param user_type: 帐号类型
    """
    account_type = new_input('请选择要创建的帐号类型[{}]>>>: '.format('|'.join(settings.USER_TYPE_LIST))) \
        if user_type is None else user_type
    if account_type in settings.USER_TYPE_LIST:
        account = new_input('请设置帐号>>>: ') if user_name is None else user_name
        if account not in settings.ACCOUNTS_DATA:
            pwd = new_input('请设置不小于6位数的登录密码>>>: ')
            if len(pwd) >= 6:
                print('[{}]帐号注册成功，类型为[{}]'.format(account, account_type))
                settings.ACCOUNTS_DATA[account] = {'pwd': pwd, 'type': account_type}
            else:
                print('密码不符合要求')
        else:
            print('[{}]帐号已存在'.format(account))
    else:
        print('帐号类型错误')

