#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/24
# Location: DongGuang
# Desc:     检测帐号是否存在


import os
from conf import settings


def is_exist(user):
    """
    检测帐号是否存在
    :param user: 检测帐号
    :return: 用户文件路径 or None
    """
    account_list = os.listdir(settings.ACCOUNT_PATH)
    user_file_name = '{}.json'.format(user)
    if user_file_name in account_list:
        return '{}\{}'.format(settings.ACCOUNT_PATH, user_file_name)
    else:
        return None


def get_user_db_file(user):
    """
    获取用户信息文件
    :param user: 帐号
    :return: user_db
    """
    pass
