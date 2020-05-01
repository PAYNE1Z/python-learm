#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/25
# Location: DongGuang
# Desc:     程序主入口


import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from mall.bin import mall
from atm.bin import atm
from atm.manage import atm_manage
from modules.logger import log


def show_menu():
    """输出引导菜单"""
    usage = """
    \n-----中国红太阳集团-----
    1. 购物商城
    2. ATM (提现、转帐、还款)
    3. ATM管理后台
    4. 退出
    """
    print(usage)


def main():
    """主函数"""
    project_switch = {
        1: mall.main,
        2: atm.main,
        3: atm_manage.main
    }
    log('access', 'both').info('欢迎光临红太阳集团')
    while True:
        show_menu()
        choice = input('请输入选项[1|2|3|4]>>: ')
        if choice.isdigit():
            choice = int(choice)
            if choice in project_switch:
                project_switch[choice]()
            elif choice == 4:
                log('access', 'both').info('已退出,欢迎下次光临')
                return None
        else:
            print('[{}]无效的选项'.format(choice))


if __name__ == "__main__":
    main()