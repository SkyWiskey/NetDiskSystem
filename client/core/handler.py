import socket
import json
import os
import struct
import time

from config import settings

class Handler(object):
    def __init__(self):
        self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.username = None

    def login(self,*args):
        if len(args) != 2:
            print('格式错误，请重新输入 提示：login 用户名 密码')
            return
        username, password = args
        self.conn.send(f'login {username} {password}'.encode('utf8'))
        res = self.conn.recv(1024).decode('utf8')
        result = json.loads(res)
        if result['status']:
            print(result['data'])
            self.username = username
            return
        print(result['data'])

    def register(self,*args):
        if len(args) != 2:
            print('格式错误，请重新输入 提示：register 用户名 密码')
            return
        username,password = args
        self.conn.send(f'register {username} {password}'.encode('utf8'))
        res = self.conn.recv(1024).decode('utf8')
        result = json.loads(res)
        if result['status']:
            print(result['data'])
            return
        print(result['data'])

    def ls(self,*args):
        if not self.username:
            print('登陆后才能查看')
            return
        if not args:
            cmd = 'ls'
        elif len(args) == 1:
            cmd = 'ls {}'.format(*args)
        else:
            print('格式错误 提示：ls 或者 ls 文件夹名称')
            return
        self.conn.send(cmd.encode('utf8'))
        #接收负端发送过来的文件列表
        res = self.conn.recv(1024).decode('utf8')
        res_dict = json.loads(res)
        if res_dict['status']:
            print(res_dict['data'])
            return
        print(res_dict['data'])

    def upload(self,*args):
        if not self.username:
            print('登陆后才允许上传')
            return
        if len(args) != 2:
            print('格式错误 提示：upload 本地文件路径 远程目录')
            return
        #本地文件路径       远程文件路径
        local_file_path,remote_file_path = args
        if not os.path.exists(local_file_path):
            print(f'文件{local_file_path}不存在，请重新输入')
            return
        self.conn.send(f'upload {remote_file_path}'.encode('utf8'))
        #判断文件大小 制作报头 先发送报头
        total_size = os.path.getsize(local_file_path)
        header = struct.pack('i',total_size)
        self.conn.send(header)
        time.sleep(0.5)
        #发送数据文件
        with open(local_file_path,'rb')as f:
            for line in f:
                self.conn.send(line)
        print('上传完毕')

    def download(self,*args):
        if not self.username:
            print('登陆后才能下载')
            return
        if len(args) != 2:
            print('格式错误 提示：download 本地路径 远程目录')
            return
        local_file_path , remote_file_path = args
        folder = os.path.dirname(local_file_path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        #报头反解
        self.conn.send(f'download {remote_file_path}'.encode('utf8'))
        header = self.conn.recv(4)
        total_size = struct.unpack('i', header)[0]
        #接收数据并下载到指定路径
        with open(local_file_path,'wb')as f:
            recv_size = 0
            while recv_size < total_size:
                line = self.conn.recv(1024)
                f.write(line)
                recv_size += len(line)

        res = self.conn.recv(1024).decode('utf8')
        res_dict = json.loads(res)
        if res_dict['status']:
            print(res_dict['data'])
            return
        print(res_dict['data'])


    def run(self):
        self.conn.connect((settings.HOST,settings.PORT))
        welcome = '''
        登录：login       用户名 密码
        注册：register    用户名 密码
        查看：ls          目录
        上传：upload      本地路径 远程目录
        下载：download    本地路径 远程目录
        '''
        print(welcome)

        while True:
            text = input(f'({self.username or "未登录"})>>>').strip()
            if not text:
                print('输入不能为空,请重新输入>>>')
                continue
            if text.upper() == 'Q':
                print('quit out')
                self.conn.send('q'.encode('utf8'))
                break
            cmd,*args = text.split(' ')
            method_map = {
                'login':self.login,
                'register':self.register,
                'ls':self.ls,
                'upload':self.upload,
                'download':self.download

            }
            method = method_map.get(cmd)
            if not method:
                print('你输入的命令不存在,请重新输入>>>')
                continue
            method(*args)
        self.conn.close()