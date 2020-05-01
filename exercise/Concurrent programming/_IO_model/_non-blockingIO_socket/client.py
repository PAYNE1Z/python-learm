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
    client.send(msg.encode('utf8'))

    server_data = client.recv(1024)
    print(f'server msg: {server_data.decode("utf8")}')