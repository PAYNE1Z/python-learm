#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/24
# Location: DongGuang
# Desc:     主程序入口


import copy
from modules import login
from modules import transfer
from modules import withdrawal


def menu_window():
    """"打印功能菜单"""
    menu = """
    {}
    1. 帐号信息
    2. 转帐
    3. 提现
    """.format('Luffy Bank'.center(30, '-'))
    print(menu)


def show_account_info(data, user):
    """
    显示帐户信息
    :param: data: 用户数据
    :param: user: 用户帐号
    :return:
    """
    info = """
    {}
    [{}]帐户余额: {}
    帐户有效期：{}
    {}
    """.format('#'.center(10, '-'), user, data['amount'], data['expire_date'], '#'.center(10, '-'))
    print(info)
    return 0


@login.auth
def main(user_data, user_db):
    """
    主程序
    :param user_data: 当前登录用户的信息
    :param user_db: 登录用户信息文件
    :return
    """
    global exit_flag
    func_switch = {
         '1': show_account_info,
         '2': transfer.transfer_account,
         '3': withdrawal.cash_withdrawal
    }
    user = user_db.split('\\')[-1].split('.')[0]
    while not exit_flag:
        menu_window()
        choice = input('请选择功能选项[1|2|3]; 退出[q|Q]>>: ')
        if choice in ['q', 'Q']:
            exit('再见')
        if choice in ['1', '2', '3']:
            ret = func_switch[choice](user_data, user)
            if ret:
                user_data = copy.deepcopy(ret)
        else:
            print('没有该选项:[{}]'.format(choice))
            continue
    exit_flag = True


if __name__ == "__main__":
    exit_flag = False
    main()