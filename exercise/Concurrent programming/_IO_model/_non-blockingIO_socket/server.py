#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/5
# Location: DongGuang
# Desc:     do the right thing

""""socket默认就是阻塞连接, Linux下，可以通过设置socket使其变为non-blocking"""

from socket import *

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 8888))
server.listen(5)
server.setblocking(False)   # 设置为非阻塞模式

rlist = []  # 存放链接对象 eg: [(conn, client),(...)...]
wlist = []  # 存放链接对象与对应的send数据 eg: [(conn, data), (...)...]
del_rlist = []  # 断开的链接对象列表  eg: [conn1,conn2,...]
del_wlist = []  # 已成功发送数据的链接对象  eg: [(conn1, data), (conn2,data), ...]


while True:

    # try用来捕捉非阻塞IO模型下，用户进程向系统kernel询问数据的结果，询问没有结果时，就会返回BlockingIOError异常
    # 通过捕捉这个异常，我们就不用在原地等待结果，可以执行线程中的别的任务，如：处理已链接的客户端的数据收发
    try:
        # 1、等待链接
        conn, client = server.accept()   # accept等待客户端连接，就是阻塞IO，客户端没有链接过来，它会一直卡在这里等
        print(f'New connections for {client}')
        rlist.append((conn, client))
    # 如果还没链接过来，将会循环处理链接与各客户端交互
    except BlockingIOError:

        # 2、接收数据
        for item in rlist:
            sock, client_addr = item[0], item[1]
            try:
                data = sock.recv(1024)
                if not data: raise ConnectionError('Client actively disconnects the link')   # 客户端主动断开链接
                # 收到客端数据，就将链接对象与要发送的消息加到wlist
                wlist.append((sock, data.upper()))
            except BlockingIOError:  # 暂时没有数据，continue
                continue
            except Exception as e:  # 其它链接错误
                print(f'{client_addr} is break link; \nINFO: {e}')
                sock.close()
                # 加入断开链接对象列表，因为不能在迭代rlist时删除rlist中的对象，所以先放到一个列表中，迭代结束后再移除元素
                del_rlist.append(item)

        # 3、 发送数据
        for item in wlist:
            sock, data = item[0], item[1]
            try:
                sock.send(data)
                del_wlist.append(item)
            except BlockingIOError:
                pass

        # 4、移除已经发送成功的链接对象
        for _item in del_wlist:
            wlist.remove(_item)
        del_wlist.clear()  # 处理完后记得一定要清空这个列表

        # 5、移除断开的链接对象
        for _item in del_rlist:
            rlist.remove(_item)
        del_rlist.clear()  # 处理完后记得一定要清空这个列表


server.close()

"""
通过非阻塞IO，我们似乎实现了单线和下的多并发？这太牛了
但是非阻塞IO模型绝不被推荐。
我们不能否则其优点：能够在等待任务完成的时间里干其他活了（包括提交其他任务，也就是 “后台” 可以有多个任务在“”同时“”执行）。

但是也难掩其缺点：
1. 循环调用recv()将大幅度推高CPU占用率；这也是我们在代码中留一句time.sleep(2)的原因,否则在低配主机下极容易出现卡机情况
2. 任务完成的响应延迟增大了，因为每过一段时间才去轮询一次read操作，而任务可能在两次轮询之间的任意时间完成。
这会导致整体数据吞吐量的降低
"""