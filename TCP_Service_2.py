# -*- coding:utf-8 -*-
# 多线程服务器
from socket import *
from threading import Thread
from time import sleep
import random
import re
# 处理客户端的请求并执行事情
def dealWithClient(newSocket,destAddr):
    # 向每个连接的客户端发送30个随机数
    random_list = [random.randint(1,30) for i in range(30)]
    newSocket.send(bytes((("%s,caculate:%s" % (str(destAddr), random_list)).encode())))
    while True:
        recvData = newSocket.recv(1024)
        if recvData:
            if(recvData==' '):
                pass
            else:
                print('recv[%s]:%s'%(str(destAddr), recvData.decode()))
                pattern = re.compile(r'\d+')
                res = pattern.findall(recvData.decode())
                list=[];row=[];i=0
                for tmp in res:
                    i+=1
                    row.append(tmp)
                    if i >3:
                        list.append(row)
                        row = []
                        i=0
                print(list)
        else:
            print('[%s]客户端已经关闭'%str(destAddr))
            break
        break
        pass
    newSocket.close()
def main():
    serSocket = socket(AF_INET, SOCK_STREAM)
    serSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR  , 1)
    localAddr = ('127.0.0.1', 8080)
    serSocket.bind(localAddr)
    serSocket.listen(5)
    try:
        while True:
            print('-----主进程，%s:%s，等待新客户端的到来------'%localAddr)
            newSocket,destAddr = serSocket.accept()
            print('-----主进程，，接下来创建一个新的进程负责数据处理[%s]-----'%str(destAddr))
            client = Thread(target=dealWithClient, args=(newSocket,destAddr))
            client.start()
            #因为线程中共享这个套接字，如果关闭了会导致这个套接字不可用，
            #但是此时在线程中这个套接字可能还在收数据，因此不能关闭
            #newSocket.close()
    finally:
        serSocket.close()
if __name__ == '__main__':
    main()
