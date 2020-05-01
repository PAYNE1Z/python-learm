#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/17
# Location: DongGuang
# Desc:     logging 高阶用法


import logging
from logging import handlers



"""logger"""
# 生成logger对象
logger = logging.getLogger('test')
logger.setLevel(logging.DEBUG)  # 设置全局日志级别

# 默认日志级别为 warning : 小于warning级别的日志将被过滤
# 设置了全局日志级别后：以全局日志级别进行首次过虑
# 全局日志级别过虑后： 再经过handler对象设置的日志级别再次过滤(如果有设置的话)


"""handler"""
# 生成handler对象
ch = logging.StreamHandler()   # 输出到终端
fh = logging.FileHandler(filename='test.log')  # 输出到文件
ch.setLevel(logging.WARNING)  # 设置handler输出到终端的日志级别
fh.setLevel(logging.INFO)     # 设置handler输出到文件的日志级别

# 把handler对象绑定到logger对象
logger.addHandler(ch)
logger.addHandler(fh)


"""formatter"""
# 生成formatter对象
cf = logging.Formatter('%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s')  # 输出到终端的格式
ff = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')  # 输出到文件的格式

# 把formatter对象 绑定到handler对象
ch.setFormatter(cf)
fh.setFormatter(ff)




"""filter"""
# filter组件用于过滤包含指定字符串的日志

class IgnoreMsgFilter(logging.Filter):
    """忽略带指定字符串的日志"""
    def __init__(self, f_str):
        super().__init__()
        self.f_str = f_str

    def filter(self, record):
        return self.f_str not in record.getMessage()

# 把filter对象绑定到logger对象中
logger.addFilter(IgnoreMsgFilter('TEST MSG'))


logger.debug('this is debug messages')
logger.info('this is info messages')
logger.warning('this is warning messages')
logger.error('this is warning messages')
logger.critical('this is critical messages')
logger.critical('this is TEST MSG')




""""日志截断handlers.RotatingFileHandler"""
# 根据设置规则截断日志
# 当文件达到一定大小之后，它会自动将当前日志文件改名，
# 然后创建 一个新的同名日志文件继续输出。
# 比如日志文件是chat.log。当chat.log达到指定的大小之后，
# RotatingFileHandler自动把 文件改名为chat.log.1。
# 不过，如果chat.log.1已经存在，会先把chat.log.1重命名为chat.log.2。。。最后重新创建 chat.log，继续输出日志信息
fh_rotate = handlers.RotatingFileHandler(filename='test_rotate.log', maxBytes=10, backupCount=3)
# filename: 日志文件名
# maxBytes: 日志最大大小(超过这个大小就截断)
# backupCount: 保留多少个日志文件
fh_rotate.setLevel(logging.INFO)
fh_rotate.setFormatter(ff)
logger.addHandler(fh_rotate)


"""日志截断handlers.TimedRotatingFileHandler"""
# 根据设置规则截断日志
# 这个Handler和RotatingFileHandler类似，
# 不过，它没有通过判断文件大小来决定何时重新创建日志文件，
# 而是间隔一定时间就 自动创建新的日志文件。
# 重命名的过程与RotatingFileHandler类似，
# 不过新的文件不是附加数字，而是当前时间
fh_time_rotate = handlers.TimedRotatingFileHandler(filename='test_time_rotate.log', when='S', interval=5, backupCount=3)
# filename: 日志文件名
# when: 时间类型(S/秒 M/分 H/小时 D/天 W/周 midnight/每天凌晨)
# interval: 间隔多久就截断日志(超过这个时间就截断)
# backupCount: 保留多少个日志文件
fh_time_rotate.setLevel(logging.INFO)
fh_time_rotate.setFormatter(ff)
logger.addHandler(fh_time_rotate)


logger.warning('Rotating log file test 1')
logger.warning('Rotating log file test 2')
logger.warning('Rotating log file test 3')
logger.warning('Rotating log file test 4')
logger.warning('Rotating log file test 5')