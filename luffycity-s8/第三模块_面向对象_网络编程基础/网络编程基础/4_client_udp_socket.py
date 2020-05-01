#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/8
# Location: DongGuang
# Desc:     do the right thing

import socket

server_addr = '127.0.0.1'
server_port = 9999

### 客户端
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client.connect((server_addr, server_port))  # 不基于链接不需要建立链接

while True:
    msg = input('>>>: ').strip().encode('utf-8')
    client.sendto(msg, (server_addr, server_port))  # 直接指定服务端地址发送数据

    data, server_ip = client.recvfrom(1024)  # 接收服务端返回的数据
    print(data, server_ip)


"""
UDP基于数据报，可以发送空字符
UDP发送数据与接收数据一定是一对一的关系，有一个sendto就要有一个recvfrom
基于UDP的socket发送接收数据不会粘包，超过recvfrom接收大小的内容会被丢弃
"""