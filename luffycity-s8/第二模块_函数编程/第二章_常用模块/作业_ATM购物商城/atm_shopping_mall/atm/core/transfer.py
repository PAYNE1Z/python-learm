#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/24
# Location: DongGuang
# Desc:     转帐功能


from conf import settings
from modules import check_user_exist
from modules import serialization
from modules.logger import log
from modules.is_number import is_number


def transfer_(data, user):
    """
    转帐
    :param data: 用户数据
    :param user: 用户帐号
    :return:
    """
    log_type = 'transfer'
    to_user = input('请输入要转入帐号: ')
    to_user_db = check_user_exist.is_exist(to_user, 'get')  # 检测用户是否存在，并获取用户信息文件
    if to_user_db:
        to_user_data = serialization.load_account(to_user_db)  # 加载用户信息
        if to_user == user:
            log(log_type, 'both').info("转出[{}]转入[{}]帐号不能相同".format(user, to_user))
            return 0

        transfer_money = is_number(input('请输入转帐金额[手续费:%5]>>: '))
        if transfer_money:
            transfer_fee = transfer_money * settings.TRANSFER_FEE_RATE  # 手续费
            if transfer_money <= (transfer_fee + data['amount']):  # 转帐金额要小于余额+手续费 才能转
                data['amount'] -= (transfer_money + transfer_fee)  # 转出帐号减去转出金额与手续费
                to_user_data['amount'] += transfer_money  # 转入帐号加上转入金额
                log(log_type, 'both').info("""[{}]转出金额：[{}]; 手续费：[{}]; 当前帐号余额：[{}]""".format(
                    user, transfer_money, transfer_fee, data['amount']))
                # 保存所做修改
                log(log_type, 'file').info("""[{}]帐户转入[{}],余额:[{}]""".format(
                    to_user, transfer_money, to_user_data['amount']))
                serialization.dump_account(data, check_user_exist.is_exist(user, 'get'))
                serialization.dump_account(to_user_data, to_user_db)
                return data
            else:
                print('帐户余额不足')
                return 0
        else:
            print('请输入数字')
            return 0
    else:
        print('目标帐号不存在')
        return 0
