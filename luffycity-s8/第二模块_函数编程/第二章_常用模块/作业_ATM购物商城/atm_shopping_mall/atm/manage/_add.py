#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/27
# Location: DongGuang
# Desc:     新增帐户


import os
import datetime
from conf import settings
from modules.logger import log
from modules import md5
from modules import check_user_exist
from modules import serialization


def make_data(user_type, user_db_path, log_type, user_pass):
    """
    生成帐户字典
    :param user_type: 用户类型
    :param user_db_path: 用户数据文件
    :param log_type: 日志类型（日志打到哪个文件）
    :param user_pass: 用户明文密码
    :return: user_data 用户数据字典
    """
    user_id = len(os.listdir(user_db_path)) + 1  # id自增
    term_of_validity = settings.TERM_OF_VALIDITY  # 帐号有效期
    today = datetime.datetime.now()
    if term_of_validity[-1] == 'D':
        offset = datetime.timedelta(days=int(term_of_validity.split('D')[0]))
    elif term_of_validity[-1] == 'H':
        offset = datetime.timedelta(hours=int(term_of_validity.split('H')[0]))
    elif term_of_validity[-1] == 'M':
        offset = datetime.timedelta(minutes=int(term_of_validity.split('M')[0]))
    else:
        log(log_type, 'both').error('时间格式错误')
        return 0
    expire_date = (today + offset).strftime('%Y-%m-%d')
    user_pass_md5 = md5.make_md5(user_pass)
    user_data = {
        "status": 0,
        "expire_date": "{}".format(expire_date),
        "id": "{}".format(user_id),
        "password": "{}".format(user_pass_md5),
        "quota": "{}".format(settings.INIT_QUOTA),
        "amount": "".format(settings.INIT_QUOTA)
    }
    if user_type == 'admin':
        user_data.pop('amount')  # admin帐号无需这两项
        user_data.pop('quota')

    return user_data


def add_account(log_type):
    """新增帐号"""
    user_type = input('请输入要新增的用户类型[user|admin]>>: ')
    if user_type in ['user', 'admin']:
        user_db_path = settings.ADMIN_ACCOUNT_PATH if user_type == 'admin' else settings.USER_ACCOUNT_PATH
        user_name = input('请输入用户名>>: ')
        if not check_user_exist.is_exist(user_name, 'check'):
            while True:
                user_pass = input('请输入密码>>: ')
                user_pass_confirm = input('请再次输入密码确认>>:')
                user_db_name = '{}.json'.format(user_name)
                if user_pass == user_pass_confirm:
                    choice = input('新增{}类型帐号[{}]; 确认请按[y|Y]>>: '.format(user_type, user_name))
                    if choice in ['y', 'Y']:
                        user_db_file = r'{}\{}'.format(user_db_path, user_db_name)
                        user_data = make_data(user_type, user_db_path, log_type, user_pass)
                        serialization.dump_account(user_data, user_db_file)
                        log(log_type, 'both').info('[{}]帐号创建成功: {}'.format(user_name, user_data))
                        break
                    else:
                        print('无效的选项')
                else:
                    print('两次输入密码不一致')
        else:
            print('[{}]该帐号已存在'.format(user_name))
    else:
        print('没有该选项:[{}]'.format(user_type))
