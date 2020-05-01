#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/7
# Location: DongGuang
# Desc:     FTP服务端


from socket import *
import os
import struct
import json
import shutil
from multiprocessing import Process, Queue
from conf import settings
from modules.serialization import Serialize
from modules.logger import log
from modules.get_md5 import GetMD5
from modules.get_dir_attr import GetDirAttr
from modules.get_partition_size import get_partition_free_space
from modules.size_format import SizeUnitFormat

SizeFormat = SizeUnitFormat()


class FTPServer:
    socket_family = AF_INET    # socket族类
    socket_type = SOCK_STREAM  # socket类型
    allow_reuse_addr = True  # 是否开启端口快速回收复用
    MAX_PACKET_SIZE = 8196   # 单次收发包的最大字节
    ACCESS_LOG = 'access'  # 访问日志文件名
    ERROR_LOG = 'error'   # 错误日志文件名

    def __init__(self, server_addr, server_port, bind_and_listen=True):
        """初始化服务端对象与socket"""
        self.server_address = (server_addr, server_port)
        self.server_port = server_port
        self.socket = socket(self.socket_family, self.socket_type)
        self.USER_DATA = Serialize.load(settings.USER_DB)  # 加载帐户数据
        self.conn = None
        self.client = None
        self.login_user = None  # 当前登录用户
        self.login_user_info = None  # 当前登录用户信息
        self.login_user_home_path = None  # 当前登录用户家目录绝对路径
        self.login_user_work_path = None  # 当前登录用户当前目录绝对路径
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

    def close_accept(self):
        """关闭链接"""
        self.conn.close()
        log(self.ACCESS_LOG, 'both').info('{}链接已关闭'.format(self.client))

    def close_server(self):
        """关闭服务端"""
        self.socket.close()

    def recv_head(self):
        """接收包头数据"""
        head_struct = self.conn.recv(4)  # 接收包头长度
        if head_struct:
            head_len = struct.unpack('i', head_struct)[0]
            # 接收包头(大于MAX_PACKET_SIZE的数据用recv_data接收)
            if head_len <= self.MAX_PACKET_SIZE:
                head_json = self.conn.recv(head_len).decode(settings.DEFAULT_CODING)
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
            data = self.conn.recv(self.MAX_PACKET_SIZE)
            recv_size += len(data)
            if save_file:
                with open(save_file, 'ab') as f:
                    f.write(data)
            else:
                recv_data += data
        return recv_data

    def send_head(self, action_type, **kwargs):
        """发送报头数据
        :param action_type: 操作类型 ['auth', 'chdir', 'quota-space', 'mkdir', 'get', 'put', 'ls']
        :param kwargs: 对应各操作类型的参数
        """
        head_dict = {'type': action_type}
        head_dict.update(kwargs)
        head_json = json.dumps(head_dict)     # 转换为字符串类型
        head_json_bytes = bytes(head_json, encoding=settings.DEFAULT_CODING)  # 转换为bytes类型
        head_struct = struct.pack('i', len(head_json_bytes))  # 打包包头字典长度
        self.conn.send(head_struct)  # 发送包头长度
        self.conn.send(head_json_bytes)  # 发送包头

    def upper_dir(self, work_dir, _dir):
        """前缀为..或/类型的上层目录处理
        :param work_dir: 当前目录
        :param _dir: 目标目录
        """
        if _dir.startswith('..'):
            if work_dir == self.login_user_home_path:  # 处于用户家目录层，不能再往上走了
                return [self.login_user_home_path, None]
            if _dir in ['..', '../']:
                return [os.path.dirname(work_dir), None]
            prefix, suffix = _dir.split('/', 1)
            if prefix == '..':
                work_dir = os.path.dirname(work_dir)  # 获取上层目录路径
                return self.upper_dir(work_dir, suffix)
        elif _dir.startswith('/'):  # 前缀为/将当前目录切到根目录，并把要切换的目标目录前面的/去掉，便于后面join路径
            return [self.login_user_home_path, _dir[1:]]
        else:
            return [work_dir, _dir]

    def _auth(self, data):
        """
        登录认证
        :param data: 指令字典
        """
        user = data.get('user')
        status_map = {
            200: '[{}]登录成功'.format(user),
            601: '密码错误',
            602: '[{}]帐号不存在'.format(user),
            603: '[{}]帐号已在[{}]登录'.format(user, self.client)
        }
        work_dir, home_dir, home_size = None, None, None
        queue = data.get('queue')
        login_user_list = queue.get(True) if not queue.empty() else []
        if user not in login_user_list:
            if user in self.USER_DATA:
                if self.USER_DATA[user].get('password') == GetMD5.get_str_md5(data.get('password')):
                    ret = 200
                    login_user_list.append(user)
                    self.login_user = user
                    self.login_user_info = self.USER_DATA.get(user)
                    self.login_user_home_path = os.path.join(settings.FTP_USER_DIR, self.login_user_info.get('home'))
                    self.login_user_work_path = self.login_user_home_path
                    work_dir = os.path.basename(self.login_user_work_path)
                    home_dir = self.login_user_info.get('home')
                    home_size = self.login_user_info.get('storage')
                    self.login_user_info['workdir'] = work_dir
                else:
                    ret = 601
            else:
                ret = 602
        else:
            ret = 603
        data.get('queue').put(login_user_list)  # 更新进程Queue
        log(self.ACCESS_LOG, 'both').info('{}'.format(status_map[ret]))
        self.send_head('auth', ret=ret, msg=status_map[ret], workdir=work_dir,
                       home=home_dir, storage=home_size, user=user)

    def _mkdir(self, data):
        """创建目录
        :param data: 指令字典
        eg: ['mkdir abc'] ['mkdir' 'abc/test']
        """
        mk_dir = data.get('mkdir')
        work_path, mk_dir = self.upper_dir(self.login_user_work_path, mk_dir)  # 处理..或/前缀的目录
        dir_path = os.path.join(work_path, mk_dir)  # 创建目录得基于当前目录而不是家目录
        if not os.path.exists(dir_path):  # 不存在同名目录与文件才能创建
            os.makedirs(dir_path, exist_ok=True)
            send_msg = '{}:[{}]目录创建成功'.format(self.login_user, mk_dir)
        else:
            send_msg = '{}:[{}]目录存在或存在相同名称的文件'.format(self.login_user, mk_dir)
        self.send_head(data.get('type'), msg=send_msg)
        log(self.ACCESS_LOG, 'file').info(send_msg)

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
        GetAttr = GetDirAttr()
        if ls_dir:  # 有指定目标目录，显示目标目录下文件
            work_path, _dir = self.upper_dir(self.login_user_work_path, ls_dir)  # 处理..或/前缀的目录
            _dir_path = os.path.join(work_path, _dir) if _dir else self.login_user_work_path
            if os.path.isdir(_dir_path):
                send_data = GetAttr.get_dir_file(_dir_path)
            else:
                ret, send_msg = False, '当前目录下没有目标目录[{}]'.format(ls_dir)
        else:  # 没有指定目标目录，显示当前录下文件与目录
            send_data = GetAttr.get_dir_file(self.login_user_work_path)
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
            work_path, _dir = self.upper_dir(self.login_user_work_path, to_dir)  # 处理..或/前缀的目录
            _dir_path = os.path.join(work_path, _dir) if _dir else self.login_user_work_path
            if os.path.isdir(_dir_path):
                work_dir = _dir_path.split(settings.FTP_USER_DIR, 1)[1]
                self.login_user_info['workdir'] = work_dir.strip('/\\')  # 去掉前后/\
            else:
                ret, send_msg = False, '当前目录下没有目标目录[{}]'.format(to_dir)
        else:  # 没有指定目标目录，切换到家目录
            self.login_user_info['workdir'] = self.login_user_info.get('home')
        # 更新用户工作目录绝对路径
        self.login_user_work_path = os.path.join(settings.FTP_USER_DIR, self.login_user_info.get('workdir'))
        self.send_head(data.get('type'), ret=ret, msg=send_msg, workdir=self.login_user_info.get('workdir'))

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
        user_used_size = GetDirAttr.get_dir_size(self.login_user_home_path)
        action, size = data.get('action'), data.get('size')
        status_map = {
            200: '{}用户存储空间调整成功'.format(self.login_user),
            601: '所在分区[{}]没有足够空间进行扩容操作'.format(SizeFormat.size2human(sys_partition_free_size)),
            602: '用户已使用空间[{}]大于调整后的空间'.format(SizeFormat.size2human(user_used_size)),
            603: '所在分区[{}]没有足够空间进行扩容操作,或用户已使用空间[{}]大小调整后的空间'.format(
                    SizeFormat.size2human(sys_partition_free_size), SizeFormat.size2human(user_used_size))
        }
        ret = 200
        if action == '+':    # 扩容
            new_size = self.USER_DATA[self.login_user]['storage'] + SizeFormat.human2size(size)
            if SizeFormat.human2size(size) < sys_partition_free_size:  # 系统分区可用空间大于扩容大小才能调整
                self.USER_DATA[self.login_user]['storage'] = new_size
            else:
                ret = 601
        elif action == '-':  # 缩容
            new_size = self.USER_DATA[self.login_user]['storage'] - SizeFormat.human2size(size)
            if new_size > user_used_size:  # 用户当前已使用空间小于缩容后的空间才能缩容
                self.USER_DATA[self.login_user]['storage'] = new_size
            else:
                ret = 602
        else:                # 直接调整
            new_size = SizeFormat.human2size(size)
            if user_used_size < new_size < sys_partition_free_size:  # 调整后的空间要大小用户已使用空间，要小于系统分区可用空间
                self.USER_DATA[self.login_user]['storage'] = new_size
            else:
                ret = 603
        log(self.ACCESS_LOG if ret == 200 else self.ERROR_LOG, 'both').info(status_map[ret])
        Serialize.dump(settings.USER_DB, self.USER_DATA)  # 保存修改
        self.send_head(data.get('type'), ret=ret, msg=status_map[ret],
                       storage=self.USER_DATA[self.login_user]['storage'])

    def _get(self, data):
        """下载文件
        :param data: 指令字典
        """
        get_file = data.get('filename')
        work_path, file = self.upper_dir(self.login_user_work_path, get_file)  # 处理..或/前缀的目录
        file_path = os.path.join(work_path, file if file else '')
        if os.path.isfile(file_path):  # 文件存在，传输文件
            file_size = os.path.getsize(file_path)
            file_md5 = GetMD5.get_file_md5(file_path)
            already_size = data.get('havesize')
            # 发送报头信息
            self.send_head(data.get('type'), ret=True, filename=os.path.basename(get_file),
                           filesize=file_size, filemd5=file_md5)
            # 发送文件
            with open(file_path, 'rb') as f:
                log(self.ACCESS_LOG, 'both').info('{}开始下载文件{}'.format(self.login_user, get_file))
                f.seek(already_size)  # 续传文件，从已下载部分开始传
                for data in f:
                    self.conn.send(data)
                log(self.ACCESS_LOG, 'both').info('{}文件{}传输完毕'.format(self.login_user, get_file))
        else:
            msg = '[{}]文件不存在'.format(get_file)
            self.send_head(data.get('type'), ret=False, msg=msg)
            log(self.ERROR_LOG, 'both').info(msg)

    def _put(self, data):
        """上传文件
        :param data: 指令字典
        """
        put_dir = data.get('putdir') if data.get('putdir') else ''   # 如果上传目录为空，值为None
        work_path, put_dir = self.upper_dir(self.login_user_work_path, put_dir)  # 处理..或/前缀的目录
        file_name, file_size, file_md5 = data.get('filename'), data.get('filesize'), data.get('filemd5')
        have_size = 0  # 初始化上传已写入的临时文件的大小为0
        temp_file_name = '.{}.temp'.format(file_name)    # 上传写入的临时文件
        if put_dir.startswith('/'):
            put_path = os.path.join(self.login_user_home_path, put_dir)  # 绝对路径则把路径拼接到家目录
        else:
            put_path = os.path.join(work_path, put_dir)  # 根目录路径则把路径拼接到当前目录
        if not os.path.isdir(put_path):
            os.makedirs(put_path, exist_ok=True)         # 上传目录不存在，则直接创建
        put_file_path = os.path.join(put_path, file_name)
        put_temp_file_path = os.path.join(put_path, temp_file_name)
        ret = False
        user_home_used_size = GetDirAttr.get_dir_size(self.login_user_home_path)
        user_home_free_size = self.login_user_info.get('storage') - user_home_used_size
        if not os.path.isfile(put_file_path):  # 文件不存在才上传
            if os.path.isfile(put_temp_file_path):  # 临时文件存在，需要续传，获取临时文件大小
                have_size = os.path.getsize(put_temp_file_path)
            if file_size-have_size < user_home_free_size:  # 文件小于家目录可用空间才让上传
                self.send_head(data.get('type'), ret=True, filename=file_name, havesize=have_size)
                self.recv_data(file_size-have_size, put_temp_file_path)
                put_file_md5 = GetMD5.get_file_md5(put_temp_file_path)
                if file_md5 == put_file_md5:  # 检验MD5
                    os.rename(put_temp_file_path, put_file_path)  # 上传完成重命名文件
                    msg = '文件[{}]上传成功,路径[{}]'.format(file_name, put_path.split(settings.FTP_USER_DIR, 1)[1])
                    ret = True
                else:
                    msg = '文件[{}]上传错误：localMD5:{}; serverMD5:{}'.format(file_name, file_md5, put_file_md5)
            else:
                msg = '{}家目录可用空间不足'.format(self.login_user)
        else:
            msg = '{}文件在{}目录下已存在'.format(file_name, put_path.split(settings.FTP_USER_DIR, 1)[1])
        # 发送报头信息
        self.send_head(data.get('type'), ret=ret, msg=msg)
        log(self.ACCESS_LOG if ret else self.ERROR_LOG, 'both').info(msg)

    def _del(self, data):
        """删除文件与目录
        :param data: 指令字典
        """
        obj_type, remove_obj = data.get('objtype'), data.get('removeobj')
        work_path, obj = self.upper_dir(self.login_user_work_path, remove_obj)  # 处理..或/前缀的目录
        obj_path = os.path.join(work_path, obj) if obj else self.login_user_work_path
        if eval('os.path.is{}(r"{}")'.format(obj_type, obj_path)):
            if obj_path == self.login_user_work_path:
                msg = '不能删除当前所在目录{}'.format(self.login_user_info.get('workdir'))
            elif obj_path == self.login_user_home_path:
                msg = '不能删除家目录{}'.format(self.login_user_info.get('home'))
            else:
                os.remove(obj_path) if obj_type == 'file' else shutil.rmtree(obj_path)
                msg = '{}:[{}]删除成功'.format(obj_type, remove_obj)
        else:
            msg = '{}:[{}]不存在'.format(obj_type, remove_obj)
        self.send_head(data.get('type'), msg=msg)

    def _mv(self, data):
        """移动文件或目录
        :param data: 指令字典
        """
        src_obj, dst_obj = data.get('srcobj'), data.get('dstobj')
        if dst_obj:
            dst_work_path, dst = self.upper_dir(self.login_user_work_path, dst_obj)  # 处理..或/前缀的目录
        else:
            dst_work_path, dst = self.login_user_info.get('workdir'), None  # 目标未指定，则为当前目录
        src_work_path, src = self.upper_dir(self.login_user_work_path, src_obj)  # 处理..或/前缀的目录
        src_path = os.path.join(src_work_path, src) if src else self.login_user_work_path
        dst_path = os.path.join(dst_work_path, dst) if dst else self.login_user_work_path
        msg = 'src对象[{}]不存在'.format(src_obj)
        if os.path.exists(src_path):  # 源路径存在
            if src_path == self.login_user_work_path:
                msg = '不能移动当前所在目录{}'.format(self.login_user_info.get('workdir'))
            elif src_path == self.login_user_home_path:
                msg = '不能移动家目录{}'.format(self.login_user_info.get('home'))
            elif src_path == dst_path:
                msg = 'src[{}]已存在当前目录'.format(src_obj)
            else:
                try:
                    if os.path.exists(dst_path):
                        if os.path.isdir(dst_path):  # 目标路径存在并且是个目录
                            shutil.move(src_path, dst_path)  # 移动
                            msg = '[{}]=>[{}]移动成功'.format(src_obj,
                                                          dst_obj if dst_obj else '当前')
                        elif os.path.isfile(dst_path):  # 目标存在且是个文件
                            msg = '目标目录[{}]下有同名文件[{}],无法移动'.format(dst_obj if dst_obj else '当前', src_obj)
                    else:  # 目标路径不存在，移动并改名
                        os.rename(src_path, dst_path)
                        msg = '[{}]=>[{}]移动并重命名成功'.format(src_obj, dst_obj if dst_obj else '当前')
                except OSError as e:
                    msg = '系统错误, {}'.format(e)
        # 发送处理结果
        log(self.ACCESS_LOG, 'both').exception(msg)
        self.send_head(data.get('type'), msg=msg)

    def update_queue(self, _queue, _type):
        """更新进程Queue中登录用户列表
        :param _queue: Queue对象
        :param _type: append or remove (目录需求只处理remove)
        """
        q_list = _queue.get(True) if not _queue.empty() else []
        try:
            eval('q_list.{}("{}")'.format(_type, self.login_user))
            log(self.ACCESS_LOG, 'both').info('[{}]退出登录'.format(self.login_user))
        except ValueError:
            pass
        _queue.put(q_list)

    def interactive(self, *args):
        """与客户端链接交互"""
        log(self.ACCESS_LOG, 'both').info(
            '子进程: {}; New connection form client: {}'.format(os.getpid(), self.client))
        while True:  # 通信循环
            try:
                head_data = self.recv_head()
                if not head_data:   # 客户端主动断开链接,抛异常集中处理
                    raise ConnectionResetError('client actively disconnected the link')
                q_data = {'queue': args[0]}
                head_data.update(q_data)  # 把进程Queue加入数据字典，在用户登录时验证是否已经登录
                func_type = '_{}'.format(head_data.get('type'))
                if hasattr(self, func_type):
                    func = getattr(self, func_type)
                    func(head_data)
            except (OSError, ConnectionError, ConnectionResetError) as e:
                # 客户端异常中断链接或主动断开: 1、将登录用户从Queue登录用户列表中删除; 2、关闭这个链接
                log(self.ACCESS_LOG, 'both').exception('lose link from client {} .. \nINFO:{}'.format(self.client, e))
                self.update_queue(args[0], 'remove')
                self.close_accept()
                break

    def run(self):
        """运行入口, 循环等待客户端连接，
        连接进来后交给子进程去处理与客户端的命令交互，达到多用户同时登录的效果
        """
        queue = Queue()   # 进程通信，用来放登录用户列表，不让一个用户多处登录
        queue.put([])     # 初始化一个Queue空列表,用来存放登录用户
        while True:       # 链接循环,等等待客户端连接
            log(self.ACCESS_LOG, 'both').info('主进程: [{}] Waiting for connections...'.format(os.getpid()))
            self.conn, self.client = self.get_accept()
            # 子进程处理客户端请求
            process = Process(target=self.interactive, args=(queue, self.conn, self.client))
            process.start()



