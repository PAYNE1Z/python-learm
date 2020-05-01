#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/25
# Location: DongGuang
# Desc:     ATM管理程序入口


import os
from modules import login
from modules.logger import log
from atm.manage import _add
from atm.manage import _quota
from atm.manage import _frozen


def show_menu():
    """"打印功能菜单"""
    menu = """
    {}
    1. 添加帐号
    2. 调整额度
    3. 冻结帐号
    """.format('ATM MANAGE'.center(30, '-'))
    print(menu)


@login.auth('admin')
def main(data, user_db):
    """
    ATM管理接口
    :param: data: 管理帐户数据
    :param: user_db: 管理帐户用户名
    :return:
    """
    global log_type
    global user
    log_type = 'ATM-manage'
    user = os.path.basename(user_db).split('.')[0]
    func_switch = {
        '1': _add.add_account,
        '2': _quota.quota_adjust,
        '3': _frozen.frozen
    }
    log(log_type, 'file').info('[{}]登录管理程序'.format(user))
    while True:
        show_menu()
        choice = input('请输入功能选项[1|2|3]; 退出[q|Q]>>: ')
        if choice in func_switch:
            func_switch[choice](log_type)
        elif choice.upper() == "Q":
            log(log_type, 'both').info('[{}]退出ATM管理程序'.format(user))
            return 0
        else:
            log(log_type, 'both').info('输入选项错误,请重新输入')
