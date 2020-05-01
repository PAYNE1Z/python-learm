#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/30
# Location: DongGuang
# Desc:     多线程实现并发socket


from socket import *


server_addr = ('127.0.0.1', 8888)
client = socket(AF_INET, SOCK_STREAM)
client.connect(server_addr)

if __name__ == "__main__":
    while True:
        try:
            text = input('>>>: ').strip()
            if not text: continue
            client.send(text.encode('utf8'))
            data = client.recv(1024)
            print(f'{data.decode("utf8")}')
        except ConnectionError as e:
            print(e)