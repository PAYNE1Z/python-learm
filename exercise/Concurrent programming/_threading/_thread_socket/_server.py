#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/30
# Location: DongGuang
# Desc:     多线程实现并发socket


from threading import Thread
from socket import *


server_addr = ('127.0.0.1', 8888)
server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(server_addr)
server.listen(5)


def connection(_conn, _client):
    """通信"""
    while True:
        try:
            data = _conn.recv(1024)
            if not data: raise AssertionError
            _conn.send(data.upper())
        except (ConnectionError, AssertionError) as e:
            print(f'{_client} Disconnected link \n INFO:{e}')
            _conn.close()
            break


if __name__ == "__main__":
    while True:  # 链接循环
        conn, client = server.accept()
        print(f'new connections from {client}')

        t = Thread(target=connection, args=(conn, client))
        t.start()