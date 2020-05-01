#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/24
# Location: DongGuang
# Desc:     主程序入口


import os
import copy
from modules import login
from modules.logger import log
from atm.core import withdrawal, transfer, repayment

def menu_window():
    """"打印功能菜单"""
    menu = """
    {}
    1. 帐号信息
    2. 转帐
    3. 提现
    4. 还款
    """.format('ATM'.center(30, '-'))
    print(menu)


def show_account_info(data, user):
    """
    显示帐户信息
    :param: data: 用户数据
    :param: user: 用户帐号
    :return:
    """
    info = """
    [{}]
    帐户状态:   {}
    帐户余额:   {}
    帐户有效期: {}
    信用额度:   {}
    """.format(user.center(20, '-'), data['status'], data['amount'], data['expire_date'], data['quota'])
    print(info)
    return 0


@login.auth('user')
def main(user_data, user_db):
    """
    主程序
    :param user_data: 当前登录用户的信息
    :param user_db: 登录用户信息文件
    :return
    """
    exit_flag = False
    func_switch = {
         '1': show_account_info,
         '2': transfer.transfer_,
         '3': withdrawal.withdrawal_,
         '4': repayment.repayment_,
    }
    user = os.path.basename(user_db).split('.')[0]
    while not exit_flag:
        menu_window()
        choice = input('请选择功能选项[1|2|3|4]; 退出[q|Q]>>: ')
        if choice.upper() == "Q":
            log('login', 'both').info('[{}]帐号退出'.format(user))
            exit_flag = True
        if choice in func_switch:
            ret = func_switch[choice](user_data, user)
            if ret:
                user_data = copy.deepcopy(ret)
        else:
            print('没有该选项:[{}]'.format(choice))
            continue

