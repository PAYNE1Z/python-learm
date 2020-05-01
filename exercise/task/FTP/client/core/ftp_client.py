#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/8
# Location: DongGuang
# Desc:     ftp客户端


from socket import *
import struct
import json
import os
import sys
import re
import time
from conf import settings
from modules.strip_input import strip_input
from modules.get_md5 import GetMD5
from modules.get_partition_size import get_partition_free_space
from modules.size_format import SizeUnitFormat
from modules.progress_bar import progress_bar
from modules.colored import Colored

SizeFormat = SizeUnitFormat()
colors = Colored()


class FTPClient:
    socket_family = AF_INET  # socket族类
    socket_type = SOCK_STREAM  # socket类型
    MAX_PACKET_SIZE = 8196  # 单次收发包的最大字节

    def __init__(self, server_addr, server_port):
        """初始客户端对象与socket"""
        self.server_address = (server_addr, server_port)
        self.server_port = server_port
        self.socket = None
        self.login_user_info = None  # 当前登录用户信息

    def __str__(self):
        return f"""
        ----- [{self.login_user_info.get('user')}]INFO -----
        HOME_DIR: {self.login_user_info.get('home')}
        WORK_DIR: {self.login_user_info.get('workdir')}
        STORAGE:  {SizeFormat.size2human(self.login_user_info.get('storage'))}
        """

    @staticmethod
    def _help(args):
        """帮助信息"""
        help_usage = """
            help command[mkdir,cd,ls,quota,get,put,mv,del,show] : 查看指定命令的帮助信息
            """
        show_usage = """
            show : 查看当前登录用户信息
            """
        mkdir_usage = """
            mkdir dirname : 创建目录
               eg: ['mkdir abc']       在当前目录下创建
                   ['mkdir /abc/test'] 在家目录下创建
                   ['mkdir ../abc']    在上层目录下创建
            """
        cd_usage = """
            cd [dirname] : 切换目录
                eg: ['cd']           切换到用户家目录
                    ['cd ../test']   切换到上层目录下的test目录
                    ['cd abc']:      切换到当前目录下abc目录
                    ['cd /abc/test'] 切换到家目录下abc/test目录
            """
        ls_usage = """
            ls [dirname] : 显示目录下文件与目录、修改时间、大小
                eg: ['ls']           显示当前目录下文件与目录
                    ['ls ..']        显示上层目录下文件与目录
                    ['ls ../test']   显示上层目录下的test目录下的文件与目录
                    ['ls abc']       显示当前目录下abc/test目录
                    ['ls /abc/test'] 显示家目录下abc/test目录
            """
        quota_usage = """
            quota action size : 调整家目录空间大小,支持单位[M,G,T]
                eg: ['quota = 500M'] 调整为500M空间
                    ['quota + 50M']  增加50M空间
                    ['quota - 50M']  减小50M空间
            """
        get_usage = """
            get file [save_dir] : 下载文件，未指定本地目录则下载到客户端定义的数据主目录下，如有指定但目录不存在将在数据目录下自动创建目录
                eg: ['get a.txt']            下载当前目录下的a.txt文件到本地当前目录
                    ['get abc/a.txt test']   下载当前目录下的abc目录下的a.txt文件到本地test目录
                    ['get /abc/a.txt']       下载家目录下的abc目录下的a.txt文件到本地当前目录
            """
        put_usage = """
            put file [remote_dir] : 上传文件,未指定远程目录则上传到用户家目录下，如有指定但目录不存在将在用户家目录下自动创建目录
                eg: ['put a.txt']                 上传默认数据目录下的a.txt文件到远程家目录
                    ['put abc/a.txt test']:       上传默认数据目录下的abc目录下的a.txt文件到远程家目录下的test目录
                    ['put /abc/a.txt /abc/test']  上传本地abc目录下的a.txt文件到远程家目录下的abc/test目录
            """
        del_usage = """
            del -f|-d del_obj : 删除家目录下文件或目录,注意：-d 删除目录时会删除目录下所有文件与目录
                eg: ['del -f a.txt']:  删除当前目录下的a.txt文件
                    ['del -d abc']:  删除当前目录下的abc目录,注意：删除目录将会删除目录下所有文件与目录
                    ['del -f /abc/a.txt']: 删除家目录下的abc目录下的a.txt文件
            """
        mv_usage = """
            mv src [dst] : 移动或重命名配家目录下文件与目录
                eg: ['mv a.txt abc']:  移动当前目录下的a.txt文件到当前目录下：如果abc不存在，则将a.txt改名为abc
                    ['mv abc /test']:  移动当前目录下的abc目录到家目录下: 如果test存在且是个目录，则将abc移动到test目录下
                    ['mv /abc/a.txt abc']: 移动家目录下的abc目录下的a.txt文件到当前目录下：如果abc存在且是个文件，将发弃这次操作
            """

        var_str = f'{args[1]}_usage' if len(args) == 2 else f'{args[0]}_usage'
        if var_str in locals():
            var = locals().get(var_str)
            print(colors.green(var))
        else:
            print(colors.red('无效的指令'))

    @staticmethod
    def re_replace(strings):
        """目录文件分隔符匹配模式，替换用户输入中的多个/与多个\统一改为/，便于后续处理与显示
        :param strings: 要处理的字符串
        :return 替换后的字符串
        """
        rc = re.compile('([/|\\\])+')
        return rc.sub('/', strings)

    @staticmethod
    def check_args(args, min_args=None, max_args=None, need_args=None):
        """检测参数合法性
        :param args:  实际传入参数
        :param min_args: 最少参数个数
        :param max_args: 最多参数个数
        :param need_args: 明确指定需要参数个数
        """
        if min_args:
            if len(args) < min_args:
                print(colors.yellow(f'最少需要{min_args}个参数,只传入{len(args)}个'))
                return False
        if max_args:
            if len(args) > max_args:
                print(colors.yellow(f'最多只需要{max_args}个参数,传入了{len(args)}个'))
                return False
        if need_args:
            if len(args) != need_args:
                print(colors.yellow(f'需要{need_args}个参数,传入了{len(args)}个'))
                return False
        return True

    def make_socket(self):
        """生成socket对象"""
        self.socket = socket(self.socket_family, self.socket_type)

    def client_connect(self):
        """连接服务端"""
        self.make_socket()
        self.socket.connect(self.server_address)

    def close_client(self):
        """关闭客户端"""
        self.socket.close()

    def send_head(self, action_type, **kwargs):
        """发送报头数据
        :param action_type: 操作类型 ['auth', 'chdir', 'quota-space', 'mkdir', 'get', 'put', 'ls']
        :param kwargs: 对应各操作类型的参数
        """
        head_dict = {'type': action_type}
        head_dict.update(kwargs)
        head_json = json.dumps(head_dict)  # 转换为字符串类型
        head_json_bytes = bytes(head_json, encoding=settings.DEFAULT_CODING)  # 转换为bytes类型
        head_struct = struct.pack('i', len(head_json_bytes))  # 打包包头字典长度
        self.socket.send(head_struct)  # 发送包头长度
        self.socket.send(head_json_bytes)  # 发送包头

    def recv_head(self):
        """接收包头数据"""
        head_struct = self.socket.recv(4)  # 接收包头长度
        if head_struct:
            head_len = struct.unpack('i', head_struct)[0]
            # 接收包头(大于MAX_PACKET_SIZE的数据用recv_data接收)
            if head_len <= self.MAX_PACKET_SIZE:
                head_json = self.socket.recv(head_len).decode(settings.DEFAULT_CODING)
            else:
                head_json = self.recv_data(head_len).decode(settings.DEFAULT_CODING)
            head_dict = json.loads(head_json)
        else:
            head_dict = {}
        return head_dict

    def recv_data(self, data_size, save_file=None):
        """接收大于单个包最大字节的数据
        :param data_size: 数据大小
        :param save_file: 写入文件
        """
        progress_gen = progress_bar(data_size)  # 创建进度条生成器对象
        next(progress_gen)  # 激活生成器
        recv_size = 0
        recv_data = b''
        while recv_size < data_size:  # 已接收的大小小于结果大小就一直收
            data = self.socket.recv(self.MAX_PACKET_SIZE)
            recv_size += len(data)
            if save_file:
                with open(save_file, 'ab') as f:
                    f.write(data)
                    progress_gen.send(recv_size)  # 传递当前进度，并输出进度条
            else:
                recv_data += data
        return recv_data

    def _auth(self):
        """登录"""
        count = 0
        while count < 3:
            count += 1
            user = strip_input(colors.blue('User>>>: '))
            pwd = strip_input(colors.blue('Password>>>: '))
            if not user or not pwd: continue
            self.send_head('auth', user=user, password=pwd)
            ret = self.recv_head()
            if ret.get('type') == 'full':  # 服务端达到并发上线
                exit(colors.yellow(ret.get('msg')))
            status = ret.get('ret')
            if status == 200:
                print(colors.green(ret.get('msg')))
                self.login_user_info = ret  # 当前登录用户信息字典
                return True
            else:
                print(colors.red(ret.get('msg')))
        else:
            print(colors.red('超过重试次数！！！'))
            return False

    def _mkdir(self, args):
        """创建目录
        :param args: 命令行信息 eg: ['mkdir abc'] ['mkdir' 'abc/test']
        """
        if self.check_args(args, need_args=2):
            self.send_head(args[0], mkdir=self.re_replace(args[1]))
            head_data = self.recv_head()
            print(head_data.get('msg'))

    def _cd(self, args):
        """切换目录
        :param args: 命令行信息
        eg:
        ['cd', ]: 不指定目录则切换到用户家目录
        ['cd', '..'] 切换到上层目录
        ['cd', '../test'] 切换到上层目录下的test目录
        ['cd', 'abc']: 切换到当前目录下abc目录
        ['cd', 'abc/test']： 切换到当前目录下abc/test目录
        ['cd', '/abc/test']： 切换到家目录下abc/test目录
        """
        if self.check_args(args, min_args=1, max_args=2):
            to_dir = None if len(args) == 1 else self.re_replace(args[1])
            self.send_head(args[0], todir=to_dir)
            head_data = self.recv_head()
            if head_data.get('ret'):
                self.login_user_info['workdir'] = head_data.get('workdir')
            else:
                print(colors.red(head_data.get('msg')))

    def _ls(self, args):
        """查看目录下文件
        :param args: 命令行信息
        eg:
        ['ls', ]: 不指定目录则列出当前目录下文件与目录
        ['ls', '..', '../'] 显示上层目录下文件与目录
        ['ls', '../test'] 显示上层目录下的test目录下的文件与目录
        ['ls', 'abc']: 显示当前目录下abc目录
        ['ls', 'abc/test']： 显示当前目录下abc/test目录
        ['ls', '/abc/test']： 显示家目录下abc/test目录
        """
        if self.check_args(args, min_args=1, max_args=2):
            ls_dir = None if len(args) == 1 else self.re_replace(args[1])
            self.send_head(args[0], lsdir=ls_dir)
            head_data = self.recv_head()
            if head_data.get('ret'):
                print(colors.green(''.join(head_data.get('data'))))
            else:
                print(colors.red(head_data.get('msg')))

    def _quota(self, args):
        """调整家目录空间，单位支持[M,G,T]
        :param args: 命令行信息
        eg:
        ['quota', '=', '500M']: 调整为500M空间
        ['quota', '+', '50M']: 增50M空间
        ['quota', '-', '50M']: 减小50M空间
        """
        if self.check_args(args, need_args=3):
            if args[1] in ['+', '-', '='] and args[2][-1] in ['M', 'G', 'T']:
                self.send_head(args[0], action=args[1], size=args[2])
                head_data = self.recv_head()
                print(head_data.get('msg'))
                if head_data.get('ret') == 200:
                    self.login_user_info['storage'] = head_data.get('storage')
            else:
                print(colors.red('命令不合法,请查看帮助信息'))

    def _get(self, args):
        """下载文件，未指定本地目录则下载到客户端定义的数据主目录下，如有指定但目录不存在将在数据目录下自动创建目录
        :param args: 命令信息
        eg:
        ['get a.txt']: 下载当前目录下的a.txt文件到本地当前目录
        ['get abc/a.txt test']: 下载当前目录下的abc目录下的a.txt文件到本地test目录
        ['get /abc/a.txt']: 下载家目录下的abc目录下的a.txt文件到本地当前目录
        """
        if self.check_args(args, min_args=2, max_args=3):
            save_path = args[2] if len(args) == 3 else settings.DEFAULT_DATA_DIR
            file = self.re_replace(args[1])  # 下载文件，可能包含路径： 'abc/test/a.txt'
            file_name = os.path.basename(file)  # 截取文件名
            if not os.path.exists(save_path):
                save_path = os.path.join(settings.DEFAULT_DATA_DIR, save_path.strip('/\\'))
                os.makedirs(save_path, exist_ok=True)
            save_file_path = os.path.join(save_path, file_name)
            download_temp_file_path = os.path.join(save_path, f'.{file_name}.temp')  # 临时文件
            have_size = 0  # 已下载大小初始为0
            if os.path.isfile(download_temp_file_path):  # 存在下载临时文件，记录已下载大小
                have_size = os.path.getsize(download_temp_file_path)

            if not os.path.isfile(save_file_path):  # 文件不存在，才继续
                self.send_head(args[0], filename=file, havesize=have_size)
                head_data = self.recv_head()
                if head_data.get('ret'):
                    file_size = head_data.get('filesize')
                    file_md5 = head_data.get('filemd5')
                    sys_partition_free_size = get_partition_free_space(save_path)

                    if sys_partition_free_size > file_size:  # 本地存储路径分区空间大于文件大小
                        # 文件不存在,看是否有临时文件
                        if os.path.isfile(download_temp_file_path):  # 临时文件存在,自动续传
                            print(colors.blue(f'检测到[{file_name}]文件的下载纪录，自动续传'))
                            if have_size < file_size:  # 检测文件没下载完才继续下载
                                print(colors.blue(f'开始续传:[{file_name}], 总大小:[{SizeFormat.size2human(file_size)}], '
                                f'续传大小:[{SizeFormat.size2human(file_size - have_size)}] ...'))
                                self.recv_data(file_size - have_size, download_temp_file_path)  # 下载剩余部分
                        else:  # 文件与临时文件都不存在就直接下载
                            print(colors.blue(f'开始下载:[{file_name}], 大小:[{SizeFormat.size2human(file_size)}] ...'))
                            self.recv_data(file_size, download_temp_file_path)

                        # 检验MD5确认文件下载完成，将临时文件改为下载文件名称
                        save_file_md5 = GetMD5.get_file_md5(download_temp_file_path)
                        if file_md5 == save_file_md5:
                            os.rename(download_temp_file_path, save_file_path)
                            print(colors.green(f'文件[{file}]下载成功,下载路径:[{save_file_path}]'))
                        else:
                            print(colors.red(f'下载出错:severMD5:{file_md5}; localMD5:{save_file_md5}'))
                    else:
                        print(colors.yellow(
                            f'本地数据目录所在分区空间[{SizeFormat.size2human(sys_partition_free_size)}]不足'))
                else:
                    print(colors.yellow(head_data.get('msg')))
            else:
                print(colors.yellow(f'本地目录[{save_path}]文件[{file_name}]已存在,请更改下载目录重试'))

    def _put(self, args):
        """上传文件，未指定远程目录则上传到用户家目录下，如有指定但目录不存在将在用户家目录下自动创建目录
        :param args: 命令信息
        eg:
        ['put a.txt']: 上传默认数据目录下的a.txt文件到远程家目录
        ['put abc/a.txt test']: 上传默认数据目录下的abc目录下的a.txt文件到远程家目录下的test目录
        ['put /abc/a.txt /abc/test']: 上传本地abc目录下的a.txt文件到远程家目录下的abc/test目录
        """
        if self.check_args(args, min_args=2, max_args=3):
            put_dir = self.re_replace(args[2]) if len(args) == 3 else None  # 未指定远程目录，传递None
            file_dir = self.re_replace(args[1])  # 上传文件，可能包含路径： 'abc/test/a.txt'
            file_name = os.path.basename(file_dir)  # 截取文件名
            if re.search('^[A-Za-z]?:|^/+', file_dir):  # 是否绝对路径 eg: F:\\abc.txt /abc.txt
                file_path = file_dir  # 绝对路径就在系统上找
            else:  # 不是绝对路径就在其默认据目录找
                file_path = os.path.join(settings.DEFAULT_DATA_DIR, file_dir)

            if os.path.exists(file_path):  # 上传文件存在
                file_size = os.path.getsize(file_path)
                file_md5 = GetMD5.get_file_md5(file_path)
                self.send_head(args[0], filename=file_name, filesize=file_size, filemd5=file_md5, putdir=put_dir)
                head_data = self.recv_head()
                if head_data.get('ret'):
                    already_size = head_data.get('havesize')
                    if already_size == 0:
                        print(colors.blue(f'开始上传[{file_name}], 大小:[{SizeFormat.size2human(file_size)}]'))
                    else:
                        print(colors.blue(f'检测到[{file_name}]文件的上传纪录，自动续传'))
                        print(colors.blue(f'开始续传[{file_name}], 总大小:[{SizeFormat.size2human(file_size)}],'
                        f'续传大小:[{SizeFormat.size2human(file_size - already_size)}]'))
                    progress_gen = progress_bar(file_size - already_size)
                    next(progress_gen)
                    send_size = 0
                    with open(file_path, 'rb') as f:
                        f.seek(already_size)
                        for data in f:
                            send_size += len(data)
                            self.socket.send(data)
                            progress_gen.send(send_size)

                    # 接收上传结果
                    head_data = self.recv_head()
                    print(colors.green(self.re_replace(head_data.get('msg'))))
                else:
                    print(colors.red(self.re_replace(head_data.get('msg'))))
            else:
                print(colors.yellow(f'{file_path}文件不存在'))

    def _del(self, args):
        """删除远程服务器文件或目录
        :param args: 命令信息
        eg:  del type[-f|-d] obj
        ['del -f a.txt']:  删除当前目录下的a.txt文件
        ['del -d abc']:  删除当前目录下的abc目录,注意：删除目录将会删除目录下所有文件与目录
        ['del -f /abc/a.txt']: 删除家目录下的abc目录下的a.txt文件
        """
        if self.check_args(args, need_args=3):
            args_map = {'-f': 'file', '-d': 'dir'}
            if args[1] in args_map:
                obj_type, remove_obj = args_map[args[1]], self.re_replace(args[2])
                _continue = True
                if obj_type == 'dir':
                    choice = strip_input(colors.yellow(
                        f'Waring:使用[-d]参数将删除[{remove_obj}]目录下所有文件与目录，确认请按[y|Y]>>: '))
                    _continue = True if choice.upper() == 'Y' else False
                if _continue:
                    self.send_head(args[0], objtype=obj_type, removeobj=remove_obj)
                    head_data = self.recv_head()
                    print(self.re_replace(head_data.get('msg')))
            else:
                print(colors.red('无效的参数'))

    def _mv(self, args):
        """移动或重命名远程服务器文件或目录
        :param args: 命令信息
        eg:  mv src [dst]
                如果 dst 不存在，将src移动到dst位置并更名为dst
                如果 dst 存在且是个目录， 则将src移动到dst目录下
                如果 dst 在在且是个文件， 则返回提示信息，不做操作

        ['mv a.txt abc']:  移动当前目录下的a.txt文件到当前目录下的abc目录
        ['mv abc /test']:  移动当前目录下的abc目录到家目录下的test目录
        ['mv /abc/a.txt abc']: 移动家目录下的abc目录下的a.txt文件到当前目录下的abc目录
        """
        if self.check_args(args, min_args=2, max_args=3):
            src_obj = self.re_replace(args[1])
            dst_obj = self.re_replace(args[2]) if len(args) == 3 else None
            self.send_head(args[0], srcobj=src_obj, dstobj=dst_obj)
            head_data = self.recv_head()
            print(self.re_replace(head_data.get('msg')))

    def _exit(self, args):
        """退出程序"""
        del args
        self.close_client()
        sys.exit('Bye...')

    def _show(self, args):
        """查看当前用户信息"""
        del args
        print(colors.blue(self))

    def run(self):
        """运行客户端"""
        # 服务端异常中断，自动重新连接
        retry_num = 0
        while retry_num < settings.RETRY_CONN_NUM:
            try:
                self.client_connect()  # 创建链接
                retry_num = 0  # 连接成功，归零
                print(colors.green(f'成功连接到服务器:[{self.server_address}]'))

                # 登录认证
                if self._auth():
                    print(colors.blue('请输入要执行的操作[help:查看帮助信息;exit:退出]'))
                    while True:
                        user = self.login_user_info['user']
                        work_dir = self.re_replace(self.login_user_info['workdir'])
                        cmds = strip_input(colors.blue(f'[{user}]:[{work_dir}]>>: '))
                        if not cmds: continue
                        cmd_list = cmds.split()
                        cmd_str = f'_{cmd_list[0]}'
                        if hasattr(self, cmd_str):
                            func = getattr(self, cmd_str)
                            func(cmd_list)
                        else:
                            print(colors.red('不支持的命令'))
            except ConnectionError as e:
                retry_num += 1
                print(colors.yellow(f'{e}\n正在尝试重新连接[{retry_num}]...'))
                self.close_client()
                time.sleep(settings.RETRY_CONN_INTERVAL)
            except EOFError or KeyboardInterrupt as e:  # pycharm:Ctrl+D；windows,linux:Ctrl+c 结束程序
                print(e, '\nBey!!!')
                self.close_client()
                break
        else:
            print(colors.red('自动重新连接失败，请检测服务端是否正常运行'))
