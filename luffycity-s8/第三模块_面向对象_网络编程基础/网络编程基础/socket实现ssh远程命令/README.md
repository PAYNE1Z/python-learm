## Python socket 实现类似于ssh执行远程服务器命令的程序


---
#### 功能需求
1. 在客户端输入一个命令，在远程服务器上执行，并获取执行结果

#### 开发环境
___
 - Windows 10
 - Python 3.5.0
 - Pycharm 2019.1

### 运行程序
___
##### 服务端
   1. 将server目录下的ssh_server.py部署到你要执行命令的远程服务器上
   2. 修改ssh_server.py的SERVER_ADDR, SERVER_PORT参数，默认为127.0.0.1:8888
   3. 运行
   `python3 ssh_server.py`
##### 客户端
   1. 将client目录下的ssh_client.py部署到你本机或者要发起命令的服务器上
   2. 修改ssh_client.py中的 SERVER_ADDR SERVER_PORT两个参数指向部署ssh_server.py的服务器与端口
   3. 运行
   `python3 ssh_client.py`

    
### 程序运行效果
___
    1. 客户端：
    请输入命令[命令长度不能超过8196字节]>>>: dir
     驱动器 F 中的卷是 Payne
     卷的序列号是 0009-C6E9
    
     F:\python-learm\luffycity-s8\第三模块_面向对象_网络编程基础\网络编程基础\socket实现ssh远程命令\server 的目录
    
    2019/07/08  PAYNE 06:55    <DIR>          .
    2019/07/08  PAYNE 06:55    <DIR>          ..
    2019/07/08  PAYNE 06:55             4,242 ssh_server.py
                   1 个文件          4,242 字节
                   2 个目录 303,880,249,344 可用字节
    
    请输入命令[命令长度不能超过8196字节]>>>: 
    
    
    2. 服务端
    from client:  ('127.0.0.1', 58663)

        