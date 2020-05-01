#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/9
# Location: DongGuang
# Desc:     创建登录帐号


import os
from conf import settings
from modules.strip_input import strip_input
from modules.size_format import SizeUnitFormat
from modules.serialization import Serialize
from modules.get_md5 import GetMD5
from modules.get_partition_size import get_partition_free_space
from modules.logger import log

SizeFormat = SizeUnitFormat()
USER_DATA = Serialize.load(settings.USER_DB)

def make_account():
    """
    创建登录帐号,与用户家目录，生成用户信息字典，序列化到文件
    """
    # FTP用户数据目录所在分区可用大小
    sys_partition_free_size = get_partition_free_space(settings.FTP_USER_DIR)

    while True:
        print('帐号配置,退出请按[b|B]'.center(30, '='))
        account = strip_input('请设置帐号>>>: ')
        if not account:continue
        if account.upper() == 'B':break

        pwd = strip_input('请设置不小于6位数的登录密码>>>: ')
        if account not in USER_DATA and len(pwd) >= 6:
            user_home = os.path.join(settings.FTP_USER_DIR, account)
            if not os.path.isdir(user_home):
                os.makedirs(user_home, exist_ok=True)  # 创建用户家目录

            allocated_size = sum(USER_DATA[user].get('storage') for user in USER_DATA)    # 已给用户分配的空间
            home_space = strip_input('所在分区可用容量:[{}],请设置存储空间大小,单位:[M,G,T],>>>: '.format(
                SizeFormat.size2human(sys_partition_free_size - allocated_size)))
            if not home_space:continue
            unit = home_space[-1]  # 单位
            space = home_space.split(unit, 1)[0]  # 数值
            if SizeFormat.is_number(space) and unit in ['M', 'G', 'T']:
                if int(space) < 1:
                    print('不能设置负大小')
                    continue
                home_size = SizeFormat.human2size(home_space)
                if home_size < sys_partition_free_size:
                    USER_DATA[account] = {'password': GetMD5.get_str_md5(pwd), 'storage': home_size, 'home': account}
                    Serialize.dump(settings.USER_DB, USER_DATA)
                    log('access', 'both').info('[{}]帐号注册成功: {}'.format(account, USER_DATA[account]))
                else:
                    log('error', 'both').info('所在分区没有[{}]的可分配空间'.format(home_space))
            else:
                log('error', 'both').info('无效的字节单位或无效的数值')
        else:
            log('error', 'both').info('[{}]帐号已存在，或密码不符合要求'.format(account))

