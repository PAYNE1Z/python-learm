#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/13
# Location: DongGuang
# Desc:     装饰器练习


"""
一、编写3个函数，每个函数执行的时间是不一样的，
    提示：可以使用time.sleep(2)，让程序sleep 2s或更多，

二、编写装饰器，为每个函数加上统计运行时间的功能
    提示：在函数开始执行时加上start=time.time()就可纪录当前执行的时间戳，函数执行结束后在time.time() - start就可以拿到执行所用时间

三、编写装饰器，为函数加上认证的功能，即要求认证成功后才能执行函数

四、编写装饰器，为多个函数加上认证的功能（用户的账号密码来源于文件），要求登录成功一次，后续的函数都无需再输入用户名和密码
"""

import time
import json

def auth(func):
    """
    装饰器：认证模块
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        account = args[0]
        global user_status
        if not user_status:
            u_name = input('username: ')
            u_pass = input('password: ')
            if u_name in account:
                if u_pass == account[u_name]['password']:
                    print('[%s]登录成功' % u_name)
                    user_status = True
            else:
                exit('帐号不存在')
        if user_status:
            print('帐号状态：已登录')
            func()

    return wrapper


def run_time(func):
    """
    装饰器：统计程序模块运行时间
    :return:
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func()
        end_time = time.time()
        print('Running time : [%s]' % (end_time - start_time))
    return wrapper

@auth
@run_time
def dinner():
    """
    吃饭
    :return:
    """
    time.sleep(4.5)
    print("It's time for #DINNER")

@run_time
def play_game():
    """
    玩游戏
    :return:
    """
    time.sleep(3.3)
    print("It's time for #PLAYGAME")

@auth
@run_time
def exercise():
    """
    运动
    :return:
    """
    time.sleep(1.8)
    print("It's time for #EXERCISE")


def main():
    try:
        with open(account_file, 'r', encoding='utf-8') as f:
            account_dict = json.load(f)
    except FileNotFoundError:
        print('帐户文件不存在')
    dinner(account_dict)
    play_game(account_dict)
    exercise(account_dict)

if __name__ == "__main__":
    account_file = 'account.json'
    user_status = False
    main()