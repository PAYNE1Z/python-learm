#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/4/27
# Location: DongGuang
# Desc:     第一模块《开发基础》 第一章《Python基础语法》 作业


"""
作业需求：
  1、编写登陆接口基础需求：
    让用户输入用户名密码
    认证成功后显示欢迎信息
    输错三次后退出

  2、程序升级需求：
    可以支持多个用户登录 (提示，通过列表存多个账户信息)
    用户3次认证失败后，退出程序，再次启动程序尝试登录时，还是锁定状态（提示:需把用户锁定的状态存到文件里）
"""

lock_file = "lock.txt"
user_list = ['Pony', 'Jack', 'Robin']
pass_list = ['123abc', 'abc123', 'abcefg']
max_retry_num = 3
user_retry_num = pass_retry_num = 0

while user_retry_num < max_retry_num:
    user_name = input('请输入用户名：')
    # 检测帐号有没有被锁定
    try:
        with open(lock_file, 'r', encoding="utf-8") as f:
            for line in f:
                if line.strip() == user_name:
                    exit("[%s]该帐号已被锁定" % user_name)
    except FileNotFoundError:
        # os.mknod(lock_file)  # windows不支持mknod方法
        # 第一次运行时，如果锁定文件不存在就创建一个空文件
        with open(lock_file, 'w') as f:
            pass

    # 检测帐号是否存在
    if user_name in user_list:

        while pass_retry_num < max_retry_num:
            user_pass = input('请输入密码：')
            # 检测密码是否正确
            if user_pass == pass_list[user_list.index(user_name)]:
                exit("HI. [%s] 欢迎登录" % user_name)
            else:
                print('密码错误，请重试')
                pass_retry_num += 1
        else:
            with open(lock_file, 'a', encoding="utf-8") as f:
                f.writelines(user_name + "\n")
            print("抱歉输入错误次数超过限制，[%s]帐号已被锁定" % user_name)

    else:
        print('[%s]用户不存在，请检查' % user_name)
    user_retry_num += 1

else:
    print("重试次数过多,请稍后再试")
