#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/27
# Location: DongGuang
# Desc:     额度调整


from modules import check_user_exist
from modules import serialization
from modules.logger import log
from modules.is_number import is_number


def quota_adjust(log_type):
    """
    额度调整
    :param: log_type: 日志类型
    """
    user_name = input('请输入要调整额度的帐号>>: ')
    ret = check_user_exist.is_exist(user_name, 'get')
    if ret:
        user_db = ret
        user_data = serialization.load_account(user_db)
        print('[{}]帐户当前额度:[{}]; 当前余额:[{}]'.format(user_name, user_data['quota'], user_data['amount']))
        quota_money = is_number(input('请输入调整后的额度>>: '))
        if quota_money:
            # 额度调整后,余额也要跟着改 = 新额度 - 已消费金额
            user_data['amount'] = quota_money - (user_data['quota'] - user_data['amount'])
            user_data['quota'] = quota_money
            # 保存修改
            serialization.dump_account(user_data, user_db)
            log(log_type, 'both').info('[{}]帐户额度已调整; 调整后额度:[{}] 余额:[{}]'.format(
                user_name, user_data['quota'], user_data['amount']))
        else:
            print('输入类型错误，请输入数字')
    else:
        print('[{}]帐号不存在'.format(user_name))