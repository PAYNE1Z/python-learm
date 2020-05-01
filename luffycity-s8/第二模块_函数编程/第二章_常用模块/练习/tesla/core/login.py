#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/24
# Location: DongGuang
# Desc:     登录认证


import time
from modules import md5
from modules import serialization
from modules import check_user_exist
from modules import logger
from conf import settings

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#
# if BASE_DIR not in sys.path:
#     sys.path.append(BASE_DIR)

log = logger.log

def auth(func):
    """
    登录验证装饰器
    :param func: 执行函数
    :return
    """
    def wrapper():
        max_retry = settings.PASSWORD_MAX_RETRY
        log_type = 'login'
        while True:
            user = input('User>>>: ')
            user_db = check_user_exist.is_exist(user)  # 检测帐号是否存在，并获取帐号文件路径
            if user_db:
                user_data = serialization.load_account(user_db)
                # print('[{}] INFO: {}'.format(user, user_data))
                if user_data['status'] == 0:  # 检测帐号是否被锁定
                    expire_date = user_data['expire_date']
                    expire_strptime = time.mktime(time.strptime(expire_date, '%Y-%m-%d'))
                    if expire_strptime > time.mktime(time.localtime()):  # 检测帐号是否已过期
                        p = 0
                        while p < max_retry:    # 密码重试
                            u_pass = input('Password>>>: ')
                            if md5.make_md5(u_pass) == user_data['password']:
                                log(log_type, 'both').info('[{}] 登录成功'.format(user))
                                return func(user_data, user_db)
                            else:
                                log(log_type, 'both').warning('密码错误，请重试')
                            p += 1
                        else:
                            user_data['status'] = 1
                            log(log_type, 'both').error('重试次数过多，帐号已被锁定')
                            # 保存所做修改
                            serialization.dump_account(user_data, user_db)
                            log(log_type, 'file').info('[{}]帐号状态已变更：[{}]'.format(user, user_data['status']))
                            exit(1)
                    else:
                        log(log_type, 'both').warning('[{}]帐号已过期'.format(user))
                        exit(1)
                else:
                    log(log_type, 'both').error('[{}]该帐号已被锁定'.format(user))
                    exit(1)
            else:
                log(log_type, 'both').warning('[{}]帐号不存在'.format(user))
                exit(1)

    return wrapper
