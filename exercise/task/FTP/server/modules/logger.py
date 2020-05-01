#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/25
# Location: DongGuang
# Desc:     日志记录


import os
import logging
from logging import handlers
from conf import settings


# class IgnoreMsgFilter(logging.Filter):
#     """忽略带指定字符串的日志"""
#     def filter(self, record):
#         return record.getMessage().strip()


def log(log_path, stdout_type):
    """
    记录日志
    :param stdout_type:  输出到文件或console  eg: both: file and console; file: file; console: console
    :param log_path:  日志文件路径
    :return:
    """
    # 创建logger对象
    logger = logging.getLogger(log_path)
    # 清理上次用过的handler
    logger.handlers.clear()
    # 设置全局日志级别
    logger.setLevel(settings.LOG_LEVEL)

    if stdout_type in ['file', 'both']:
        # 创建handler对象
        # file_handler = logging.FileHandler(log_file)
        # 带日志轮转的handler对象
        # 每天轮转一次，保留5个备份
        file_rotate_handler = handlers.TimedRotatingFileHandler(
            filename=log_path, encoding='utf8', when='D', interval=1, backupCount=5)

        # 生成formatter对象
        file_format = logging.Formatter(settings.LOG_TO_FILE_FORMAT)

        # 给handler设置日志 级别
        # file_rotate_handler.setLevel('logging.{}'.format(level.upper()))

        # 把formatter对象绑定到handler对象
        file_rotate_handler.setFormatter(file_format)

        # 把handler对象绑定到logger对象
        logger.addHandler(file_rotate_handler)
        # logger.addFilter(IgnoreMsgFilter())

    if stdout_type in ['console', 'both']:
        # 输出到终端的handler
        console_handler = logging.StreamHandler()
        console_format = logging.Formatter(settings.LOG_TO_CONSOLE_FORMAT)
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

    return logger

# log('test', 'both').info('this test message')
# log('test', 'file').info('this test message')
# log('test', 'console').info('this test message')
