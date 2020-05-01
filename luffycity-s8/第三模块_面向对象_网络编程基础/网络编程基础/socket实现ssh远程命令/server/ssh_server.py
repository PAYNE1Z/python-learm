#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/7
# Location: DongGuang
# Desc:     socket实现ssh远程命令服务端


from socket import *
import os
import subprocess
import struct
import json


class RemoteCMDServer:
    socket_family = AF_INET    # socket族类
    socket_type = SOCK_STREAM  # socket类型
    listen_queue_size = 5    # 链接排队数
    allow_reuse_addr = True  # 是否开启端口快速回收复用
    max_packet_size = 8196  # 单次接收包的最在字节

    def __init__(self, server_addr, server_port, bind_and_listen=True):
        """初始化服务端对象与socket"""
        self.server_address = (server_addr, server_port)
        self.server_port = server_port
        self.socket = socket(self.socket_family, self.socket_type)
        self.conn = None
        self.client = None
        self.os = os.name  # 系统平台
        self.default_coding = 'utf8' if self.os == 'posix' else 'gbk'  # windows默认编码:gbk, linux:utf8

        if bind_and_listen:
            self.server_bind()
            self.server_listen()
        else:
            self.close_server()
            raise

    def server_bind(self):
        """绑定服务端地址"""
        if self.allow_reuse_addr:
            self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 开启端口复用
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()

    def server_listen(self):
        """监听服务端端口"""
        self.socket.listen(self.listen_queue_size)

    def get_accept(self):
        """获取链接对象"""
        return self.socket.accept()

    def close_accept(self):
        """关闭链接"""
        self.socket.close()

    def close_server(self):
        """关闭服务端"""
        self.socket.close()

    def run_cmd(self, cmd):
        """运行命令，并返回命令结果
        :param cmd: 命令行
        ：:return cmd result
        """
        res = subprocess.Popen(
            cmd.decode(self.default_coding), shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout = res.stdout.read()
        stderr = res.stderr.read()
        if stderr:
            ret = stderr
        else:
            ret = stdout
        return ret

    def run(self):
        """运行"""
        while True:  # 链接循环
            self.conn, self.client = self.get_accept()
            print('from client: ', self.client)

            while True:  # 通信循环
                try:
                    # 接收客户端发来的命令 eg: 'ipconfig'
                    cmd = self.conn.recv(self.max_packet_size)
                    if not cmd: break

                    # 运行命令并返回运行结果给客户端（解决粘包问题）
                    ret = self.run_cmd(cmd)

                    ## 1.制作包头字典
                    head_dict = {'res_size': len(ret)}

                    ## 2.转换为字符串类型
                    head_json = json.dumps(head_dict)

                    ## 3.转换为bytes类型
                    head_json_bytes = bytes(head_json, encoding=self.default_coding)

                    ## 4.将包头字典大小打包成4个字节长度的字节流（便于客户端准确完整的接收到包头大小）
                    head_struct = struct.pack('i', len(head_json_bytes))

                    ## 5.发送包头字典长度
                    self.conn.send(head_struct)
                    ## 6.发送包头字典内容
                    self.conn.send(head_json_bytes)
                    ## 7.发送命令运行结果
                    self.conn.send(ret)

                # except Exception:  # Exception错误范围过大，会导致很多错误信息无法显示，应慎用
                except ConnectionResetError:
                    break


if __name__ == '__main__':
    SERVER_ADDR = '127.0.0.1'
    SERVER_PORT = 8888
    remote_cmd_server = RemoteCMDServer(SERVER_ADDR, SERVER_PORT)
    remote_cmd_server.run()