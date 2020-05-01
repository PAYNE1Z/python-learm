#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/4
# Location: DongGuang
# Desc:     socket 客户端


import socket

# 1.创建对象
phone = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

# 2.连接服务端
server_addr = ('127.0.0.1', 8888)
phone.connect(server_addr)

while True:
    # 3.发送消息
    msg = input('msg>>>: ').strip()
    if not msg: continue  # 如果发送空数据给服务端会造成客户端卡死
    phone.send(msg.encode('utf-8'))  # 通过网络发送的数据需为二进制类型

    # 4.接收消息
    data = phone.recv(1024)
    print('New massage from server:{}:  '.format(server_addr), data.decode('utf-8'))
    if not data:  # 数据为空就退出循环
        break

# 5.关闭客户端
phone.close()


"""
TCP是基于链接的数据流（类似管道）发送数据，所以发送与接收信息都基于链接
TCP（transport control protocol，传输控制协议）是面向连接的，面向流的，提供高可靠性服务。
收发两端（客户端和服务器端）都要有一一成对的socket，因此，发送端为了将多个发往接收端的包，
更有效的发到对方，使用了优化方法（Nagle算法），将多次间隔较小且数据量小的数据，合并成一个大的数据块，然后进行封包。
这样，接收端，就难于分辨出来了，必须提供科学的拆包机制。 即面向流的通信是无消息保护边界的。
"""