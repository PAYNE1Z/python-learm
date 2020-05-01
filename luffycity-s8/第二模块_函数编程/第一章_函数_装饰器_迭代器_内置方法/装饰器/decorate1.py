#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/13
# Location: DongGuang
# Desc:     装饰器


def login(auth_type):
    print('auth_type:', auth_type)

    def decorate_outer(func):
        print('decorate_outer:', func)

        def decorate_inner(*args, **kwargs):
            print('decorate_inner:', args)
            _user_name = 'robin'
            _user_pass = 'abc123'
            global user_status
            if not user_status:
                u_name = input('username: ')
                u_pass = input('password: ')
                if u_name == _user_name and u_pass == _user_pass:
                    if auth_type == 'qq':
                        print('welcome [%s] from %s' % (u_name, auth_type.upper()))
                    elif auth_type == 'weixin':
                        print('welcome [%s] from %s' % (u_name, auth_type.upper()))
                    elif auth_type == 'weibo':
                        print('welcome [%s] from %s' % (u_name, auth_type.upper()))
                    user_status = True
                else:
                    exit('username or password is wrong')

            if user_status:
                print('[%s] has logged on' % _user_name)
                func(*args, **kwargs)

        return decorate_inner

    return decorate_outer


def home():
    print(' home'.rjust(20,'-'))

@login('qq')
def science_fiction(*args, **kwargs):
    print(' science fiction'.rjust(20,'-'))
    for area in args:
        print('# ', area)

def literary():
    print(' literary'.rjust(20,'-'))

@login('weixin')
def movement():
    print(' movement'.rjust(20,'-'))

@login('weibo')
def gunplay():
    print(' gunplay'.rjust(20,'-'))

def funny():
    print(' funny'.rjust(20,'-'))


user_status = False

home()
science_fiction('CN','US','EN')
literary()
movement()
gunplay()
funny()