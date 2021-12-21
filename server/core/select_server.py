import select
import socket
from config import settings



class SelectServer(object):
    def __init__(self):
        self.socket_object_list = [] #服务端队列以及 监听的的客户端队列
        self.conn_handler_map = {}   #映射方法


    def run(self,handler):
        server_object = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_object.bind((settings.HOST,settings.PORT))
        server_object.listen(5)
        self.socket_object_list.append(server_object)

        while True:
            r,w,e = select.select(self.socket_object_list,[],[])
            for sock in r:
                #如果有连接 就进行连接 然后把conn放入sock_object_list中
                if sock == server_object:
                    print('There is a new connection...')
                    conn,addr = server_object.accept()
                    self.socket_object_list.append(conn)
                    #每个conn键对应的值都是调用PanHandler类并实例化conn
                    self.conn_handler_map[conn] = handler(conn)
                    continue
                #对每个sock_object_list中的对象都调用PanHandler类并实例化
                handler_object = self.conn_handler_map[sock]
                #执行execute方法
                result = handler_object.execute()
                #如果没有结果 就删除这个对象
                if not result:
                    self.socket_object_list.remove(sock)
                    del self.conn_handler_map[sock]
