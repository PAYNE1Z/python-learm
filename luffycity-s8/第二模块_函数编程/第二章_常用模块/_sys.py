#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/15
# Location: DongGuang
# Desc:     sys模块


import sys

print(sys.argv)       # 命令行参数List，第一个元素是程序本身路径
# sys.exit(2)    # 退出程序，正常退出时exit(0)
print(sys.version)    # 获取Python解释程序的版本信息
print(sys.maxsize)     # 最大的Int值  py2 为 sys.maxint
print(sys.path)       # 返回模块的搜索路径，初始化时使用PYTHONPATH环境变量的值
print(sys.platform)   # 返回操作系统平台名称

sys.stdout.write('please:')         # 标准输出 , 引出进度条的例子， 注，在py3上不行，可以用print代替
val = sys.stdin.readline()[:-1]     # 标准输入
sys.getrecursionlimit()             # 获取最大递归层数
sys.setrecursionlimit(1200)         # 设置最大递归层数
sys.getdefaultencoding()            # 获取解释器默认编码
sys.getfilesystemencoding()         # 获取内存数据存到文件里的默认编码


