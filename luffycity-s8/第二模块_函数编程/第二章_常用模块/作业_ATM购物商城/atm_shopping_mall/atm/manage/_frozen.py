#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/27
# Location: DongGuang
# Desc:     冻结帐号


from modules import check_user_exist
from modules import serialization
from modules.logger import log


def frozen(log_type):
    """
    冻结帐户
    :param log_type: 日志类型（日志写到哪里）
    :return:
    """
    user_name = input('请输入要冻结或解冻的帐号>>: ')
    user_db = check_user_exist.is_exist(user_name, 'get')
    if user_db:
        user_data = serialization.load_account(user_db)
        status_map = {
            0: '正常',
            1: '冻结状态'
        }
        user_status = status_map[user_data['status']]
        print('[{}]当前状态: [{}]'.format(user_name, user_status))
        choice = input('确认修改[{}]帐户状态，请按[y|Y]; 返回[b|B]>>: '.format(user_name))
        if choice.upper() == 'Y':
            user_data['status'] = 0 if user_data['status'] == 1 else 1
            serialization.dump_account(user_data, user_db)
            log(log_type, 'both').info('[{}]帐号状态已修改为:[{}]'.format(user_name, status_map[user_data['status']]))
        elif choice.upper() == 'B':
            return 0
        else:
            print('[{}]错误的选项'.format(choice))
    else:
        print('[{}]帐号不存在'.format(user_name))