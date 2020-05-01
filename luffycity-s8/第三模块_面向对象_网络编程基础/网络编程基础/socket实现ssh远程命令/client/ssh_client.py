#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/8
# Location: DongGuang
# Desc:     ssh远程执行命令客户端


from socket import *
import os
import struct
import json


class RemoteCMDClient:
    socket_family = AF_INET    # socket族类
    socket_type = SOCK_STREAM  # socket类型
    max_packet_size = 8196  # 单次接收包的最在字节

    def __init__(self, server_addr, server_port, connect=True):
        """初始客户端对象与socket"""
        self.server_address = (server_addr, server_port)
        self.server_port = server_port
        self.socket = socket(self.socket_family, self.socket_type)
        self.os = os.name  # 系统平台
        self.default_coding = 'utf8' if self.os == 'posix' else 'gbk'  # windows默认编码:gbk, linux:utf8

        if connect:
            self.client_connect()
        else:
            self.close_client()

    def client_connect(self):
        """连接服务端"""
        self.socket.connect(self.server_address)

    def close_client(self):
        """关闭客户端"""
        self.socket.close()

    def run(self):
        while True:  # 通信循环
            # 发送命令 eg: 'ipconfig'
            cmd = input('请输入命令[命令长度不能超过{}字节]>>>: '.format(self.max_packet_size)).strip()
            if not cmd or len(cmd) > 8196: continue
            self.socket.send(cmd.encode(self.default_coding))

            # 接收命令执行结果
            ## 1.先接收包头长度(4)
            head_struct = self.socket.recv(4)

            ## 2.解析包头字典长度
            head_len = struct.unpack('i', head_struct)[0]

            ## 3.接收包头字典
            head_json = self.socket.recv(head_len).decode(self.default_coding)
            head_dict = json.loads(head_json)

            ## 4.解析包头，获取命令执行结果长度
            ret_size = head_dict['res_size']

            ## 5.接收命令执行结果
            recv_size = 0
            ret_data = b''
            while recv_size < ret_size:  # 已接收的大小小于结果大小就一直收
                data = self.socket.recv(self.max_packet_size)
                recv_size += len(data)
                ret_data += data

            ## 6.输出结果
            print(ret_data.decode(self.default_coding))


if __name__ == '__main__':
    SERVER_ADDR = '127.0.0.1'
    SERVER_PORT = 8888
    remote_cmd_client = RemoteCMDClient(SERVER_ADDR, SERVER_PORT)
    remote_cmd_client.run()