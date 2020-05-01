#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/4
# Location: DongGuang
# Desc:     socket 服务端


import socket

# 1，创建对象（买电话）
phone = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
phone.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 端口快速回收复用（类似于linux内核参数）


# 2. 绑定主机端口,让客户端能找到自己（装电话卡）
phone.bind(('127.0.0.1', 8888))


# 3. 监听端口 (开机)
phone.listen(5)  # 5代表在允许有5个连接排队，更多的新连接连进来时就会被拒绝


print('start...')
while True:  # 多连接循环(排队接收多个客户端，第一个客户端断开后才处理第二个，以此类推
    # 4. 等待客户端连接：建立连接（等电话打进来）
    # 阻塞直到有连接为止，有了一个新连接进来后，就会为这个请求生成一个连接对象conn
    conn,client = phone.accept()
    print('Client: ', client)

    # 5. 收信息（接听电话）
    while True:  # 通信循环
        """
        在linux系统中如果客户端断开了连接，那么服务端在recv的时候将会进入死循环
        针对windows与linux系统在通信循环中应该防止此情况出现
        """
        try:
            data = conn.recv(1024)  # 1.接收数据单位：bytes; 2.限制最大接收数据为1024 bytes
            if not data: break  # 适用于linux(linux系统中客户端断开后data为空，服务端不会报错，需要手动判断并做处理
            print('New message from client:{}: '.format(client), data.decode('utf-8'))

            # 发信息
            conn.send(data.upper())  # 将接收到的数据转换成大写发给客户端
        except ConnectionResetError:  # 适用于windows（windows系统中客户端断开后会抛出异常）
            # ConnectionResetError: [WinError 10054] 远程主机强迫关闭了一个现有的连接。
            break


    # 6. 关闭连接 (挂电话)
    conn.close()


# 7. 关闭服务端（关机）
phone.close()