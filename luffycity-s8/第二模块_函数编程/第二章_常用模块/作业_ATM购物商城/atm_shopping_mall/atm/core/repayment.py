#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/25
# Location: DongGuang
# Desc:     还款


from modules.logger import log
from modules import serialization
from modules import check_user_exist
from modules.is_number import is_number


def repayment_(data, user):
    """
    还款接口
    :param data: 用户数据
    :param user: 用户帐号
    :return:
    """
    print(data)
    print(user)
    log_type = 'repayment'
    repay_money = is_number(input('请输入还款金额>>: '))
    if repay_money:
        # 还款入帐
        data['amount'] += repay_money
        log(log_type, 'both').info('[{}]还款: [{}]; 帐户余额: [{}]'.format(
            user, repay_money, data['amount']))
        # 保存修改
        serialization.dump_account(data, check_user_exist.is_exist(user, 'get'))
    else:
        log(log_type, 'both').info('输入类型错误,请输入数字')
    return data, user
