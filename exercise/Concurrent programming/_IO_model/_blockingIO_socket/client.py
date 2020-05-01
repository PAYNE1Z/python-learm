#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/5
# Location: DongGuang
# Desc:     do the right thing

""""socket默认就是阻塞连接"""

from socket import *

server_addr = ('127.0.0.1', 8888)
client = socket(AF_INET, SOCK_STREAM)
client.connect(server_addr)
print(f'Connections to {server_addr}')

while True:
    msg = input('>>>: ').strip()
    if not msg: continue
    client.send(msg.encode('utf8'))    # send发送数据从本地程序copy数据到系统缓冲区速度非常快，但它也是阻塞IO

    server_data = client.recv(1024)    # recv等待客户发送数据过来，也是阻塞IO，客户端不发数据过来，就一直卡在这里等
    print(f'server msg: {server_data.decode("utf8")}')