#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/24
# Location: DongGuang
# Desc:     检测帐号是否存在


import os
from conf import settings


def is_exist(user, _type, user_type='user'):
    """
    检测帐号是否存在或返回帐号文件路径
    :param user: 检测帐号
    :param _type:  [check|get] 检测帐号是否存在｜获取帐号文件
    :param user_type:  [user|admin] 用户或管理员帐号
    :return: 用户文件路径 or True or False
    """
    account_path = settings.USER_ACCOUNT_PATH if user_type == 'user' else settings.ADMIN_ACCOUNT_PATH
    account_list = os.listdir(account_path)
    user_file_name = '{}.json'.format(user)
    if user_file_name in account_list:
        if _type == 'check':
            return True
        elif _type == 'get':
            return '{}\{}'.format(account_path, user_file_name)
        else:
            return False
