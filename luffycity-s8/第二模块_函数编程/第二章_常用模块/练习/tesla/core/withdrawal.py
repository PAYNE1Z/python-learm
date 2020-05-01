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
from modules import logger

log = logger.log

def cash_withdrawal(data, user):
    """
    提现
    :param data: 用户数据
    :param user: 用户帐号
    :return:
    """
    log_type = 'withdrawal'
    withdrawal_fee_rate = settings.WITHDRAWAL_FEE_RATE
    withdrawal_amount = input('请输入提现金额：')
    if withdrawal_amount.isdigit():
        withdrawal_amount = int(withdrawal_amount)
        if withdrawal_amount <= data['amount']:
            data['amount'] -= withdrawal_amount  # 帐户减去提现金额
            data['amount'] -= withdrawal_amount * withdrawal_fee_rate  # 帐户减去提现手续费
            log(log_type, 'both').info("""[{}]提现: [{}]; 手续费: [{}]; 帐户余额: [{}]""".format(
                user, withdrawal_amount, withdrawal_amount * withdrawal_fee_rate, data['amount']))
            # 保存修改
            serialization.dump_account(data, check_user_exist.is_exist(user))
            return data
        else:
            log(log_type, 'both').info('帐户余额不足')
            return 0
    else:
        log(log_type, 'both').info('不合法的输入,请输入数字')
        return 0
