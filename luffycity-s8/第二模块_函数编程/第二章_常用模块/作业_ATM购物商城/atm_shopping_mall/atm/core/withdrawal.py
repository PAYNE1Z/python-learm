#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/24
# Location: DongGuang
# Desc:     提现功能


from conf import settings
from modules import serialization
from modules import check_user_exist
from modules.logger import log
from modules.is_number import is_number


def withdrawal_(data, user):
    """
    提现
    :param data: 用户数据
    :param user: 用户帐号
    :return:
    """
    log_type = 'withdrawal'
    withdrawal_amount = is_number(input('请输入提现金额：'))
    if withdrawal_amount:
        withdrawal_fee = withdrawal_amount * settings.WITHDRAWAL_FEE_RATE  # 手续费
        if withdrawal_amount <= (data['amount'] + withdrawal_fee):
            data['amount'] -= (withdrawal_amount + withdrawal_fee)  # 帐户减去提现金额与手续费
            log(log_type, 'both').info("""[{}]提现: [{}]; 手续费: [{}]; 帐户余额: [{}]""".format(
                user, withdrawal_amount, withdrawal_fee, data['amount']))
            # 保存修改
            serialization.dump_account(data, check_user_exist.is_exist(user, 'get'))
            return data
        else:
            log(log_type, 'both').info('帐户余额不足')
            return 0
    else:
        log(log_type, 'both').info('不合法的输入,请输入数字')
        return 0
