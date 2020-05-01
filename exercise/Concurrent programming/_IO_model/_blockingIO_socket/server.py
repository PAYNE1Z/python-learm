#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/5
# Location: DongGuang
# Desc:     do the right thing

""""socket默认就是阻塞连接"""

from socket import *

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 8888))
server.listen(5)


while True:
    conn, client = server.accept()   # accept等待客户端连接，就是阻塞IO，客户端没有链接过来，它会一直卡在这里等
    print(f'New connections for {client}')

    while True:
        try:
            data = conn.recv(1024)    # recv等待客户发送数据过来，也是阻塞IO，客户端不发数据过来，就一直卡在这里等
            if not data: continue
            conn.send(data.upper())   # send发送数据从本地程序copy数据到系统缓冲区速度非常快，但它也是阻塞IO
        except Exception as e:
            print(f'{client} is break link; \nINFO: {e}')
            conn.close()
            break


"""
在阻塞IO模型下，socket服务端一次只能与一个客户端链接进行交互

一个简单的解决方案：
在服务器端使用多线程（或多进程）。多线程（或多进程）的目的是让每个连接都拥有独立的线程（或进程），
这样任何一个连接的阻塞都不会影响其他的连接。

该方案的问题是：
开启多进程或都线程的方式，在遇到要同时响应成百上千路的连接请求，则无论多线程还是多进程都会严重占据系统资源，
降低系统对外界响应效率，而且线程与进程本身也更容易进入假死状态。

改进方案：
很多程序员可能会考虑使用“线程池”或“连接池”。“线程池”旨在减少创建和销毁线程的频率，
其维持一定合理数量的线程，并让空闲的线程重新承担新的执行任务。“连接池”维持连接的缓存池，尽量重用已有的连接、
减少创建和关闭连接的频率。这两种技术都可以很好的降低系统开销，都被广泛应用很多大型系统，如websphere、tomcat和各种数据库等。

改进后方案其实也存在着问题：
“线程池”和“连接池”技术也只是在一定程度上缓解了频繁调用IO接口带来的资源占用。而且，所谓“池”始终有其上限，
当请求大大超过上限时，“池”构成的系统对外界的响应并不比没有池的时候效果好多少。所以使用“池”必须考虑其面临的响应规模，
并根据响应规模调整“池”的大小。

"""