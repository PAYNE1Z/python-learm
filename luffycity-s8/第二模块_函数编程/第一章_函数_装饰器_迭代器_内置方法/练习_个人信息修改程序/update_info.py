#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/10
# Location: DongGuang
# Desc:     练习题<修改个人信息程序>

"""
需求：
    一、输入用户名密码，正确后登录系统 ，打印
        1. 修改个人信息
        2. 打印个人信息
        3. 修改密码
    二、每个选项写一个方法
    三、登录时输错3次退出程序

初始数据：
    jack,123456,马云,55,Alibaba,CEO,13929291399
    pony,abc123,马化腾,48,Tencent,CEO,18933992288
    robin,123abc,李彥宏,51,Baidu,CEO,18666881688
"""

def load_account(file):
    """
    从文件加载帐户数据
    :param file: 帐户文件
    :return: 帐户数据字典
    返回数据示例：
    {'robin':
          {'chinese': '李彥宏',
           'phone': '18666881688',
           'age': '51',
           'company': 'Baidu',
           'password': '123abc',
           'position': 'CEO'},
     ...
    }
    """
    personal_dict = {}
    personal_key = ['password', 'chinese', 'age', 'company', 'position', 'phone']
    with open(file, 'r', encoding='utf8') as f:
        for line in f:
            personal_info = line.strip().split(',')
            personal_dict[personal_info[0]] = dict(zip(personal_key, personal_info[1:]))
    return personal_dict


def echo_menu_info():
    """
    打印菜单信息
    :return:
    """
    info = """
    1. 打印个人信息
    2. 修改个人信息
    3. 修改密码
    4. 退出
    """
    print(info)


def echo_personal_info(data, user):
    """
    打印登录用户信息
    :param data: 帐户字典
    :param user: 登录用户
    :return:
    """
    user_dict = data[user]
    info = """
    ###: {}
    Chinese:    {}
    Company:    {}
    Age :       {}
    Job :       {}
    Phone:      {}
    --------------------
    """.format(user,
               user_dict['chinese'],
               user_dict['company'],
               user_dict['age'],
               user_dict['position'],
               user_dict['phone'])
    print(info)


def change_personal_info(data, user):
    """
    修改当前用户帐户信息
    :param data: 所有帐户信息字典
    :param user: 当前用户
    :return:
    """
    global account_dict
    user_info = data[user]  # 当前登录用户的信息
    echo_personal_info(data, user)
    while True:
        choice = input('Please select the field to modify; Press [b] to back>>>: ').lower()
        if choice in user_info:
            print('Current value: {}'.format(user_info[choice]))
            new_value = input('New value>>>: ')
            user_info[choice] = new_value  # 将修改后的值存入当前用户信息字典中
            account_dict[user] = user_info  # 将修改后的当前用户信息更新到全局所有用户信息字典中
            print('user:[{}] {} is changed.\nNew: {}'.format(user, choice, user_info))
            break
        elif choice == 'b':
            break
        else:
            print('Option is invalid')


def change_password(data, user):
    """
    修改当前用户密码
    :param data: 所有帐户信息字典
    :param user: 当前用户
    :return:
    """
    x = y = 0
    global account_dict
    while x < max_retry:
        user_pass = input('Please enter your current password for confirmation>>>: ')
        if user_pass == data[user]['password']:
            while y < max_retry:
                new_pass = input('Please enter a new password>>>: ')
                new_pass_affirm = input('Please enter your new password again>>>: ')
                if new_pass == new_pass_affirm:
                    account_dict[user]['password'] = new_pass
                    print('user:[{}] password is changed'.format(user))
                    x = 3
                    break
                else:
                    print('The passwords entered twice do not match')
                y += 1
            else:
                print('Too many retries...')
                x = 3
        else:
            print('Password error. Please try again')
        x += 1


def save_change():
    """
    将修改后的数据写入文件
    :return:
    """
    personal_key = ['password', 'chinese', 'age', 'company', 'position', 'phone']
    user_info = []
    with open(account_file, 'r+', encoding='utf-8') as f:
        f.seek(0)
        f.truncate()
        # 将字典转换为单个用户信息列表，再转为字符串，写入文件
        for k in account_dict:
            user_info.append(k)
            for x in personal_key:
                user_info.append(account_dict[k][x])
            lines = ','.join(user_info)
            f.write('{}\n'.format(lines))
            user_info = []


def exiting(*args):
    """
    程序退出时对修改进行存档
    :return:
    """
    save_change()
    exit('Bey')


def main():
    """
    程序入口
    :return:
    """
    global exit_flag
    count = 0
    action_list = {
        1: echo_personal_info,
        2: change_personal_info,
        3: change_password,
        4: exiting,
    }
    while count < max_retry:
        user_name = input('UserName>>>: ')
        user_pass = input('Password>>>: ')
        if user_name in account_dict and user_pass == account_dict[user_name]['password']:
            print('Welcome {}'.center(30, '-').format(user_name))
            while not exit_flag:
                echo_menu_info()
                choice = input('Please select number [1,2,3,4]>>>:')
                if choice.isdigit():
                    choice = int(choice)
                    if choice in [1,2,3,4]:
                        action_list[choice](account_dict, user_name)
                else:
                    print('Option is invalid')
        else:
            print('Account or Password error. Please try again')
        count += 1
    else:
        exit('Too many retries...')


if __name__ == "__main__":
    account_file = 'account.txt'
    max_retry = 3
    exit_flag = False
    account_dict = load_account(account_file)
    main()