#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/8
# Location: DongGuang
# Desc:     udp socket


import socket

server_addr = '127.0.0.1'
server_port = 9999

### 服务端
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp协议 socket类型为: SOCK_DGRAM
server.bind((server_addr, server_port))  # 服务地址与端口

# server.listen(5)   # udp基于数据报，不需要建立链接
# server.accept()

while True:
    data, client_addr = server.recvfrom(1024)  # udp不基于链接，所以直接用server对象接收
    print(data, client_addr)

    server.sendto(data.upper(), client_addr)  # 因为不基于链接，所以发送数据要指定客户端地址



