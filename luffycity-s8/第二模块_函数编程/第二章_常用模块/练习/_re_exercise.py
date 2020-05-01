#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/20
# Location: DongGuang
# Desc:     re模块练习


import re


# 1、验证手机号是否合法
phone_pattern = re.compile('(13|18|15|17)\d{9}')

def check_phone(number):
    ret = phone_pattern.fullmatch(number)
    return True if ret else False

phone = '186668866882'
if check_phone(phone):
    print('{} is a legitimate phone number'.format(phone))




# 2、验证邮箱是否合法
email_pattern = re.compile('\w+@\w+\.(com|cn|net|com\.cn|xyz)')

def check_email(address):
    ret = email_pattern.fullmatch(address)
    return True if ret else False

email = 'Payne123@gmail.xyz'
if check_email(email):
    print('{} is a legitimate email address'.format(email))
