#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/2
# Location: DongGuang
# Desc:     基于gevent实现socket服务端并发


from gevent import monkey;

monkey.patch_all()
import gevent
from socket import *


# 如果不想用money.patch_all()打补丁,可以用gevent自带的socket
# from gevent import socket
# s=socket.socket()

def server(ip, port):
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen(5)

    while True:
        try:
            conn, client = s.accept()
            print(f'New connection for {client}')
            gevent.spawn(interactive, conn, client)
        except Exception as e:
            print(e)


def interactive(conn, client):
    while True:
        try:
            data = conn.recv(1024)
            print(f'{client} msg: {data.decode("utf8")}')
            conn.send(data.upper())
        except Exception as e:
            print(e)
            conn.close()
            break


if __name__ == "__main__":
    server('127.0.0.1', 8888)