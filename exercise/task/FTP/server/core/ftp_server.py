#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/7
# Location: DongGuang
# Desc:     基于线程池实现socket并发的FTP服务端


from socket import *
import os
import struct
import json
import shutil
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, local, Lock, currentThread
import queue
from conf import settings
from modules.serialization import Serialize
from modules.logger import log
from modules.get_md5 import GetMD5
from modules.get_dir_attr import GetDirAttr
from modules.get_partition_size import get_partition_free_space
from modules.size_format import SizeUnitFormat

SizeFormat = SizeUnitFormat()
local_data = local()  # 线程信息隔离
mutex = Lock()  # 用户数据表存档互斥锁


class FTPServer:
    socket_family = AF_INET  # socket族类
    socket_type = SOCK_STREAM  # socket类型
    allow_reuse_addr = True  # 是否开启端口快速回收复用
    MAX_PACKET_SIZE = 8196  # 单次收发包的最大字节

    def __init__(self, server_addr, server_port, bind_and_listen=True):
        """初始化服务端对象与socket"""
        self.server_address = (server_addr, server_port)
        self.server_port = server_port
        self.socket = socket(self.socket_family, self.socket_type)
        self.USER_DATA = Serialize.load(settings.USER_DB)  # 加载帐户数据
        self.login_user_list = []  # 已登录用户列表
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
        self.socket.listen(settings.MAX_QUEUE_SIZE)

    def get_accept(self):
        """获取链接对象"""
        return self.socket.accept()

    @staticmethod
    def close_accept(_conn):
        """关闭链接"""
        _conn.close()
        log(settings.ACCESS_LOG_FILE, 'both').info(f'{local_data.client} 链接已关闭')

    def close_server(self):
        """关闭服务端"""
        self.socket.close()

    def recv_head(self):
        """接收包头数据"""
        head_struct = local_data.conn.recv(4)  # 接收包头长度
        if head_struct:
            head_len = struct.unpack('i', head_struct)[0]
            # 接收包头(大于MAX_PACKET_SIZE的数据用recv_data接收)
            if head_len <= self.MAX_PACKET_SIZE:
                head_json = local_data.conn.recv(head_len).decode(settings.DEFAULT_CODING)
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
        recv_size = 0
        recv_data = b''
        while recv_size < data_size:  # 已接收的大小小于数据大小就一直收
            data = local_data.conn.recv(self.MAX_PACKET_SIZE)
            recv_size += len(data)
            if save_file:
                with mutex:
                    with open(save_file, 'ab') as f:
                        f.write(data)
            else:
                recv_data += data
        return recv_data

    @staticmethod
    def send_head(action_type, **kwargs):
        """发送报头数据
        :param action_type: 操作类型 ['auth', 'chdir', 'quota-space', 'mkdir', 'get', 'put', 'ls']
        :param kwargs: 对应各操作类型的参数
        """
        head_dict = {'type': action_type}
        head_dict.update(kwargs)
        head_json = json.dumps(head_dict)  # 转换为字符串类型
        head_json_bytes = bytes(head_json, encoding=settings.DEFAULT_CODING)  # 转换为bytes类型
        head_struct = struct.pack('i', len(head_json_bytes))  # 打包包头字典长度
        local_data.conn.send(head_struct)  # 发送包头长度
        local_data.conn.send(head_json_bytes)  # 发送包头

    def upper_dir(self, _dir):
        """基于当前工作目录，处理前缀为..或/类型的上层目录处理
        :param _dir: 目标目录
        :return abs_dir_path 目录的绝对路径
        """
        if _dir.startswith('..'):
            if local_data.abs_work_path == local_data.abs_home_path:  # 处于用户家目录层，不能再往上走了
                return os.path.join(local_data.abs_home_path, _dir[3:])
            if _dir in ['..', '../']:  # 目录路径为 .. 或 ../ 直接返回当前工作目录
                return os.path.dirname(local_data.abs_work_path)
            prefix, suffix = _dir.split('/', 1)
            if prefix == '..':
                local_data.abs_work_path = os.path.dirname(local_data.abs_work_path)  # 获取上层目录路径
                return self.upper_dir(suffix)
        elif _dir.startswith('/'):  # 前缀为/将当前目录切到根目录，并把要切换的目标目录前面的/去掉，便于后面join路径
            return os.path.join(local_data.abs_home_path, _dir[1:])
        else:
            return os.path.join(local_data.abs_work_path, _dir)

    def _auth(self, data):
        """
        登录认证
        :param data: 指令字典
        """
        user = data.get('user')
        status_map = {
            200: f'[{user}]登录成功',
            601: '密码错误',
            602: f'[{user}]帐号不存在',
            603: f'[{user}]帐号已在[{local_data.client}]登录'
        }
        auth_data = {}
        if user not in self.login_user_list:
            if user in self.USER_DATA:
                if self.USER_DATA[user].get('password') == GetMD5.get_str_md5(data.get('password')):
                    ret = 200
                    self.login_user_list.append(user)
                    local_data.user = user
                    local_data.abs_home_path = local_data.abs_work_path = self.USER_DATA[user]['abs_home_path']
                    local_data.work_dir = local_data.home_dir = self.USER_DATA[user]['home']
                    local_data.storage = self.USER_DATA[user]['storage']
                    auth_data = {'user': user, 'workdir': local_data.work_dir,
                                 'hom': local_data.home_dir, 'storage': local_data.storage}
                else: ret = 601
            else: ret = 602
        else: ret = 603
        print(f'已登录用户: {self.login_user_list}')
        log(settings.ACCESS_LOG_FILE, 'both').info(f'{status_map[ret]}')
        self.send_head('auth', ret=ret, msg=status_map[ret], **auth_data)

    def _mkdir(self, data):
        """创建目录
        :param data: 指令字典
        eg: ['mkdir abc'] ['mkdir' 'abc/test']
        """
        mk_dir = data.get('mkdir')
        mk_dir_path = self.upper_dir(mk_dir)  # 处理..或/前缀的目录
        if not os.path.exists(mk_dir_path):  # 不存在同名目录与文件才能创建
            os.makedirs(mk_dir_path, exist_ok=True)
            send_msg = f'{local_data.user}:[{mk_dir}]目录创建成功'
        else:
            send_msg = f'{local_data.user}:[{mk_dir}]目录存在或存在相同名称的文件'
        self.send_head(data.get('type'), msg=send_msg)
        log(settings.ACCESS_LOG_FILE, 'file').info(send_msg)

    def _ls(self, data):
        """
        显示目录下文件与目录
        不使用系统命令获取，通过os.walk方法获取
        :param data: 指令字典
        eg:
        ['ls', ]: 不指定目录则列出当前目录下文件与目录
        ['ls', '..', '../'] 显示上层目录下文件与目录
        ['ls', '../test'] 显示上层目录下的test目录下的文件与目录
        ['ls', 'abc']: 显示当前目录下abc目录
        ['ls', 'abc/test']： 显示当前目录下abc/test目录
        ['ls', '/abc/test']： 显示家目录下abc/test目录
        """
        ls_dir = data.get('lsdir')
        ret, send_msg, send_data = True, None, None
        get_attr = GetDirAttr()
        if ls_dir:  # 有指定目标目录，显示目标目录下文件
            ls_dir_path = self.upper_dir(ls_dir)  # 处理..或/前缀的目录
            if os.path.isdir(ls_dir_path):
                send_data = get_attr.get_dir_file(ls_dir_path)
            else:
                ret, send_msg = False, f'当前目录下没有目标目录[{ls_dir}]'
        else:  # 没有指定目标目录，显示当前录下文件与目录
            send_data = get_attr.get_dir_file(local_data.abs_work_path)
        self.send_head(data.get('type'), ret=ret, msg=send_msg, data=send_data)

    def _cd(self, data):
        """切换目录
        :param data: 指令字典
          eg:
        ['cd', ]: 不指定目录则切换到用户家目录
        ['cd', '..'] 切换到上层目录
        ['cd', '../test'] 切换到上层目录下的test目录
        ['cd', 'abc']: 切换到当前目录下abc目录
        ['cd', 'abc/test']： 切换到当前目录下abc/test目录
        ['cd', '/abc/test']： 切换到家目录下abc/test目录
        """
        to_dir = data.get('todir')
        ret, send_msg = True, None
        if to_dir:  # 有指定目标目录，切换到目标目录
            to_dir_path = self.upper_dir(to_dir)  # 处理..或/前缀的目录
            if os.path.isdir(to_dir_path):
                work_dir = to_dir_path.split(settings.FTP_USER_DIR, 1)[1]
                local_data.work_dir = work_dir.strip('/\\')  # 去掉前后/\
            else:
                ret, send_msg = False, f'当前目录下没有目标目录[{to_dir}]'
        else:  # 没有指定目标目录，切换到家目录
            local_data.work_dir = local_data.home_dir
        # 更新用户工作目录绝对路径
        local_data.abs_work_path = os.path.join(settings.FTP_USER_DIR, local_data.work_dir)
        self.send_head(data.get('type'), ret=ret, msg=send_msg, workdir=local_data.work_dir)

    def _quota(self, data):
        """调整家目录存储空间
        真实环境下，调整空间需要考虑家目录所在分区是否有足够空间，并运用quota命令对用户家目录请行空间限制与调整
        这里不做那么复杂，使用虚拟空间实现
        :param data: 指令字典
        eg: 单位支持[M,G,T]
        ['quota', '=', '500M']: 调整为500M空间
        ['quota', '+', '50M']: 增50M空间
        ['quota', '-', '50M']: 减小50M空间
        """
        used_size = sum(self.USER_DATA[user].get('storage') for user in self.USER_DATA)  # 所有用户已分配大小
        sys_partition_free_size = get_partition_free_space(settings.FTP_USER_DIR) - used_size  # 所在分区可用大小
        user_used_size = GetDirAttr.get_dir_size(local_data.abs_home_path)
        action, size = data.get('action'), data.get('size')
        status_map = {
            200: f'{local_data.user}用户存储空间调整成功',
            601: f'所在分区[{SizeFormat.size2human(sys_partition_free_size)}]没有足够空间进行扩容操作',
            602: f'用户已使用空间[{SizeFormat.size2human(user_used_size)}]大于调整后的空间',
            603: f'所在分区[{SizeFormat.size2human(sys_partition_free_size)}]没有足够空间进行扩容操作',
            604: f'用户已使用空间[{SizeFormat.size2human(user_used_size)}]大于调整后的空间'
        }
        ret = 200
        if action == '+':  # 扩容: 系统分区可用空间大于扩容大小才能调整
            new_size = local_data.storage + SizeFormat.human2size(size)
            if SizeFormat.human2size(size) > sys_partition_free_size: ret = 601

        elif action == '-':  # 缩容: 用户当前已使用空间小于缩容后的空间才能缩容
            new_size = local_data.storage - SizeFormat.human2size(size)
            if new_size < user_used_size: ret = 602

        else:  # = 直接调整: 调整后的空间要大于用户已使用空间, 并要小于所在分区可用空间
            new_size = SizeFormat.human2size(size)
            if new_size > sys_partition_free_size: ret = 603
            if user_used_size > new_size: ret = 604

        log(settings.ACCESS_LOG_FILE if ret == 200 else settings.ERROR_LOG_FILE, 'both').info(status_map[ret])
        if ret == 200:
            self.USER_DATA[local_data.user]['storage'] = new_size
            local_data.storage = new_size
            with mutex:
                Serialize.dump(settings.USER_DB, self.USER_DATA)  # 保存修改
        self.send_head(data.get('type'), ret=ret, msg=status_map[ret],
                       storage=local_data.storage)

    def _get(self, data):
        """下载文件
        :param data: 指令字典
        """
        get_file = data.get('filename')
        file_path = self.upper_dir(get_file)  # 处理..或/前缀的目录
        if os.path.isfile(file_path):  # 文件存在，传输文件
            file_size = os.path.getsize(file_path)
            file_md5 = GetMD5.get_file_md5(file_path)
            already_size = data.get('havesize')
            # 发送报头信息
            self.send_head(data.get('type'), ret=True, filename=os.path.basename(get_file),
                           filesize=file_size, filemd5=file_md5)
            # 发送文件
            with mutex:
                with open(file_path, 'rb') as f:
                    log(settings.ACCESS_LOG_FILE, 'both').info(f'{local_data.user}开始下载文件{get_file}')
                    f.seek(already_size)  # 续传文件，从已下载部分开始传
                    for data in f:
                        local_data.conn.send(data)
                    log(settings.ACCESS_LOG_FILE, 'both').info(f'{local_data.user}文件{get_file}传输完毕')
        else:
            msg = f'[{get_file}]文件不存在'
            self.send_head(data.get('type'), ret=False, msg=msg)
            log(settings.ERROR_LOG_FILE, 'both').info(msg)

    def _put(self, data):
        """上传文件
        :param data: 指令字典
        """
        put_dir = data.get('putdir')
        if put_dir:  # 如果上传目录为空，值为None
            if put_dir.startswith('/'):  # 绝对路径则把路径拼接到家目录, 根目录路径则把路径拼接到当前目录
                put_path = self.upper_dir(put_dir)  # 处理..或/前缀的目录
            else:
                put_path = os.path.join(local_data.abs_work_path, put_dir)
        else:
            put_path = local_data.abs_work_path

        file_name, file_size, file_md5 = data.get('filename'), data.get('filesize'), data.get('filemd5')
        have_size = 0  # 初始化上传已写入的临时文件的大小为0
        temp_file_name = f'.{file_name}.temp'  # 上传写入的临时文件
        if not os.path.isdir(put_path): os.makedirs(put_path, exist_ok=True)  # 上传目录不存在，则直接创建
        put_file_path = os.path.join(put_path, file_name)
        put_temp_file_path = os.path.join(put_path, temp_file_name)
        ret = False
        user_home_used_size = GetDirAttr.get_dir_size(local_data.abs_home_path)
        user_home_free_size = local_data.storage - user_home_used_size
        if not os.path.isfile(put_file_path):  # 文件不存在才上传
            if os.path.isfile(put_temp_file_path):  # 临时文件存在，需要续传，获取临时文件大小
                have_size = os.path.getsize(put_temp_file_path)
            if file_size - have_size < user_home_free_size:  # 文件小于家目录可用空间才让上传
                self.send_head(data.get('type'), ret=True, filename=file_name, havesize=have_size)
                self.recv_data(file_size - have_size, put_temp_file_path)
                put_file_md5 = GetMD5.get_file_md5(put_temp_file_path)
                if file_md5 == put_file_md5:  # 检验MD5
                    os.rename(put_temp_file_path, put_file_path)  # 上传完成重命名文件
                    msg = f'文件[{file_name}]上传成功,路径[{put_path.split(settings.FTP_USER_DIR, 1)[1]}]'
                    ret = True
                else:
                    msg = f'文件[{file_name}]上传错误：localMD5:{file_md5}; serverMD5:{put_file_md5}'
            else:
                msg = f'{local_data.user}家目录可用空间不足'
        else:
            msg = f'{file_name}文件在{put_path.split(settings.FTP_USER_DIR, 1)[1]}目录下已存在'
        # 发送报头信息
        self.send_head(data.get('type'), ret=ret, msg=msg)
        log(settings.ACCESS_LOG_FILE if ret else settings.ERROR_LOG_FILE, 'both').info(msg)

    def _del(self, data):
        """删除文件与目录
        :param data: 指令字典
        """
        obj_type, remove_obj = data.get('objtype'), data.get('removeobj')
        obj_path = self.upper_dir(remove_obj)  # 处理..或/前缀的目录
        if eval(f'os.path.is{obj_type}(r"{obj_path}")'):
            if obj_path == local_data.abs_work_path:
                msg = f'不能删除当前所在目录{local_data.work_dir}'
            elif obj_path == local_data.abs_home_path:
                msg = f'不能删除家目录{local_data.home_dir}'
            else:
                os.remove(obj_path) if obj_type == 'file' else shutil.rmtree(obj_path)
                msg = f'{obj_type}:[{remove_obj}]删除成功'
        else:
            msg = f'{obj_type}:[{remove_obj}]不存在'
        self.send_head(data.get('type'), msg=msg)

    def _mv(self, data):
        """移动文件或目录
        :param data: 指令字典
        """
        src_obj, dst_obj = data.get('srcobj'), data.get('dstobj')
        # 目标未指定，则为当前目录
        dst_path = self.upper_dir(dst_obj) if dst_obj else local_data.abs_work_path
        src_path = self.upper_dir(src_obj)  # 处理..或/前缀的目录
        msg = f'src对象[{src_obj}]不存在'
        if os.path.exists(src_path):  # 源路径存在
            if src_path == local_data.abs_work_path:
                msg = f'不能移动当前所在目录{local_data.work_dir}'
            elif src_path == local_data.abs_home_path:
                msg = f'不能移动家目录{local_data.home_dir}'
            elif src_path == dst_path:
                msg = f'src[{src_obj}]已存在当前目录'
            else:
                try:
                    if os.path.exists(dst_path):
                        if os.path.isdir(dst_path):  # 目标路径存在并且是个目录
                            print(src_path, dst_path)
                            shutil.move(src_path, dst_path)  # 移动
                            msg = f'[{src_obj}]=>[{dst_obj if dst_obj else "当前"}]移动成功'
                        elif os.path.isfile(dst_path):  # 目标存在且是个文件
                            msg = f'目标目录[{dst_obj if dst_obj else "当前"}]下有同名文件[{src_obj}],无法移动'
                    else:  # 目标路径不存在，移动并改名
                        os.rename(src_path, dst_path)
                        msg = f'[{src_obj}]=>[{dst_obj if dst_obj else "当前"}]移动并重命名成功'
                except OSError as e:
                    msg = f'系统错误, {e}'
        # 发送处理结果
        log(settings.ACCESS_LOG_FILE, 'both').exception(msg)
        self.send_head(data.get('type'), msg=msg)

    def logout(self):
        """客户端断开链接或退出登录
        断开链接的情况下有可能还没有登录，所以删除时要判断是否有这个变量，否则会出错"""
        user = local_data.user if 'user' in local_data.__dict__ else None
        if user in self.login_user_list:
            self.login_user_list.remove(user)
            log(settings.ACCESS_LOG_FILE, 'both').info(f'[{user}] logout!!!')

    def interactive(self, **kwargs):
        """与客户端链接交互"""
        local_data.conn = kwargs['conn']
        local_data.client = kwargs['client']
        q = kwargs['queue']
        log(settings.ACCESS_LOG_FILE, 'both').info(
            f'{currentThread().name}: {os.getpid()}; New connection form client: {local_data.client}')

        while True:  # 通信循环
            try:
                head_data = self.recv_head()
                if not head_data:  # 客户端主动断开链接,抛异常集中处理
                    raise ConnectionResetError('client actively disconnected the link')
                func_type = f'_{head_data.get("type")}'

                if hasattr(self, func_type):
                    func = getattr(self, func_type)
                    func(head_data)
            except (OSError, ConnectionError, ConnectionResetError) as e:
                # 客户端异常中断链接或主动断开: 1、用户从已登录用户列表中删除; 2、关闭这个链接；3、退出通信循环
                log(settings.ERROR_LOG_FILE, 'both').exception(
                    f'lose link from client {local_data.client} .. \nINFO: {e}')
                self.logout()
                self.close_accept(local_data.conn)
                if not q.empty(): q.get()  # 使用队列控制并发数，需要在客户端断开链接时从队列取一个值
                break

    def run(self):
        """运行入口, 循环等待客户端连接，
        连接进来后交给子进程去处理与客户端的命令交互，达到多用户同时登录的效果
        """
        # 创建线程池对象
        # 1、用 ThreadPoolExecutor线程池实现控制并发链接数
        # executor = ThreadPoolExecutor(max_workers=settings.MAX_CONCURRENCY)

        # 2、用 queue队列实现控制并发链接数
        pool_queue = queue.Queue(maxsize=settings.MAX_CONCURRENCY)

        # 链接循环,等等待客户端连接
        while True:
            log(settings.ACCESS_LOG_FILE, 'both').info(
                f'{currentThread().name}: [{os.getpid()}] Waiting for connections...')
            conn, client = self.get_accept()

            # 多线程处理客户端请求
            # thread 方式
            thread = Thread(target=self.interactive, kwargs={'conn': conn, 'client': client, 'queue': pool_queue})
            if not pool_queue.full():
                pool_queue.put(thread)  # 链接一个客端就放入队列
                thread.start()
            else:
                local_data.conn = conn
                self.send_head('full', msg='服务端并发链接数已达上限，请稍后再试')
            # 进程池方式
            # executor.submit(self.interactive, conn=conn, client=client)
