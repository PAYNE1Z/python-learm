#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/16
# Location: DongGuang
# Desc:     配置文件处理模块 configparser



"""
ConfigParser模块在python中用来读取配置文件，配置文件的格式跟windows下的ini配置文件相似，可以包含一个或多个节(section), 每个节可以有多个参数（键=值）。
使用的配置文件的好处就是不用在程序员写死，可以使程序更灵活。
注意：在python 3 中ConfigParser模块名已更名为configparser


[DEFAULT]                   ->  sections
ServerAliveInterval = 45    ->  options / 键值对
Compression = yes
CompressionLevel = 9
ForwardX11 = yes

[bitbucket.org]
User = hg

[topsecret.server.com]
Port = 50022
ForwardX11 = no
"""

import configparser


config = configparser.ConfigParser()
config.read('config.ini')

sections = config.sections()
print('获取配置文件所有的section', sections)

options = config.options('topsecret.server.com')
print('获取指定section下所有option', options)

items = config.items('topsecret.server.com')
print('获取指定section下所有的键值对', items)

value = config.get('bitbucket.org', 'user')
print('获取指定的section下的option', type(value), value)



# 解析配置文件
print(config.sections())         # 调用sections方法(默认不会读取default)
# ['bitbucket.org', 'topsecret.server.com']

if 'bitbucket.org' in config: pass  # 判断元素是否在sections列表内
# True

print(config['bitbucket.org']['User'])  # 通过字典的形式取值
print(config['DEFAULT']['Compression'])
topsecret = config['topsecret.server.com']
print(topsecret['ForwardX11'])
print(topsecret['Port'])

for key in config['bitbucket.org']:  # for循环 bitbucket.org 字典的key
    print(key)



# 增删改查
########## 读 ##########
secs = config.sections()
print(secs)
options = config.options('bitbucket.org')  # 获取指定section的keys
print(options)

item_list = config.items('bitbucket.org')  # 获取指定 section 的 keys & values ,key value 以元组的形式
print(item_list)

val = config.get('topsecret.server.com','ForwardX11')  # 获取指定的key的value
print(val)
val = config.getint('topsecret.server.com','port')  # 获取可以int的key的value
print(val)

########## 改写 #########
sec = config.remove_section('test1')  # 删除section 并返回状态(true, false)
config.write(open('test.cfg', "w"))       # 对应的删除操作要写入文件才会生效

sec = config.has_section('wupeiqi')  # 检查section是否存在
sec = config.add_section('wupeiqi')  # 新增Section
config.write(open('test.cfg', "w"))

config.set('test','k2','21111')      # 在指定section里面新增key value  (不能是数字)
config.write(open('test.cfg', "w"))

config.remove_option('test','k1')    # 删除指定section里面的某个key
config.write(open('test.cfg', "w"))


"""
关于 [DEFAULT]
    [DEFAULT] 一般包含 ini 格式配置文件的默认项，所以 configparser 部分方法会自动跳过这个 section 。 
    前面已经提到 sections() 是获取不到的，
    还有删除方法对 [DEFAULT] 也无效：
    但指定删除和修改 [DEFAULT] 里的 keys & values 是可以的：
    还有个特殊的是，has_section() 也无效，可以和 in 区别使用
"""