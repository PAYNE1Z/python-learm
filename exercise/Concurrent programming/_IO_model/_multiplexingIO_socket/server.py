#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/5
# Location: DongGuang
# Desc:     do the right thing

""""
select模块的使用
select会监听socket或者文件描述符的I/O状态变化，并返回变化的socket或者文件描述符对象

select(rlist, wlist, xlist[, timeout]) -> (rlist, wlist, xlist)

这是Python select方法的原型，接收4个参数
rlist：list类型，监听其中的socket或者文件描述符是否变为可读状态，返回那些可读的socket或者文件描述符组成的list
wlist：list类型，监听其中的socket或者文件描述符是否变为可写状态，返回那些可写的socket或者文件描述符组成的list
xlist：list类型，监听其中的socket或者文件描述符是否出错，返回那些出错的socket或者文件描述符组成的list
timeout：设置select的超时时间，设置为None代表永远不会超时，即阻塞。
注意：Python的select方法在Windows和Linux环境下的表现是不一样的，
    Windows下它只支持socket对象，不支持文件描述符（file descriptions)，而Linux两者都支持。

我们可以通过打印来查看select模块提供的作用
1、他返回的rlist,wlist只会返回有改变的监听对象,如果没有改变的函数,那么整个程序会阻塞住
2、如果我们想要加入新的连接,那么我们只需要把连接对象放进rlist即可，
    当有数据过来的时候,那么连接就会发生改变(文件描述符),select函数就会帮我们监听到
3、如果我们想发送数据,那么我们可以把conn加入到wlist,因为发送数据需要我们去输出流数据,
    然后等待select把wlist里面的消息取出来,我们就可以发送数据了！



强调：
1. 如果处理的连接数不是很高的话，
   使用select/epoll的web server不一定比使用multi-threading + blocking IO的web server性能更好，可能延迟还更大。
   select/epoll的优势并不是对于单个连接能处理得更快，而是在于能处理更多的连接。
2. 在多路复用模型中，对于每一个socket，一般都设置成为non-blocking，
   但是，如上图所示，整个用户的process其实是一直被block的。只不过process是被select这个函数block，而不是被socket IO给block。

结论: select的优势在于可以处理多个连接，不适用于单个连接
"""

from socket import *
import select

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 8888))
server.listen(5)
server.setblocking(False)
print('starting...')

rlist = [server, ]
wlist = []
wdata = {}

while True:
    rl, wl, el = select.select(rlist, wlist, [], 0.5)
    if el: print('exceptionable: ', el)

    for sock in rl:  # 初始状态下rlist中有个server对象
        print('readable: ', rl)
        if sock == server:  # 如果是server就接收链接
            conn, client = sock.accept()
            rlist.append(conn)  # 并链接对象放到rlist交给select去监听
        else:
            try:            # 如果不是server对象，那就是链接conn对象了，在这接收数据
                data = sock.recv(1024)
                if not data: raise ConnectionError('Client actively disconnects the link')
                wlist.append(sock)   # 接收数据成功，就把conn对象放入wlist交给select监听
                wdata[sock] = data.upper()   # 把接收的数据转换成大写再放入wdata字典中
            except Exception as e:
                print(f'client break link {e}')
                sock.close()
                rlist.remove(sock)   # 客户断开链接要把链接对象从rlist中删掉，并关掉这个链接
                continue

    for sock in wl:   # 当select监听到数据准备就绪了，就发送数据
        print('writeable: ', wl)
        try:
            sock.send(wdata[sock])
            wlist.remove(sock)   # 发送成功后将链接对象从wlist与wdata中删除
            wdata.pop(sock)
        except Exception:
            pass


server.close()

"""
select监听fd变化的过程分析：

用户进程创建socket对象，拷贝监听的fd到内核空间，每一个fd会对应一张系统文件表，内核空间的fd响应到数据后，
就会发送信号给用户进程数据已到；
用户进程再发送系统调用，比如（accept）将内核空间的数据copy到用户空间，同时作为接受数据端内核空间的数据清除，
这样重新监听时fd再有新的数据又可以响应到了（发送端因为基于TCP协议所以需要收到应答后才会清除）。

该模型的优点：
相比其他模型，使用select() 的事件驱动模型只用单线程（进程）执行，占用资源少，不消耗太多 CPU，同时能够为多客户端提供服务。
如果试图建立一个简单的事件驱动的服务器程序，这个模型有一定的参考价值。

该模型的缺点：
首先select()接口并不是实现“事件驱动”的最好选择。因为当需要探测的句柄值较大时，select()接口本身需要消耗大量时间去轮询各个句柄。
很多操作系统提供了更为高效的接口，如linux提供了epoll，BSD提供了kqueue，Solaris提供了/dev/poll，…。
如果需要实现更高效的服务器程序，类似epoll这样的接口更被推荐。遗憾的是不同的操作系统特供的epoll接口有很大差异，
所以使用类似于epoll的接口实现具有较好跨平台能力的服务器会比较困难。
其次，该模型将事件探测和事件响应夹杂在一起，一旦事件响应的执行体庞大，则对整个模型是灾难性的。
"""