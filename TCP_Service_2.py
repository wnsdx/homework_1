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
    randomList = [random.randint(1,30) for i in range(30)]
    for randonNum in randomList:
        newSocket.send(bytes((("%s,caculate:%s" % (str(destAddr), randonNum)).encode())))
        while True:
            recvDate = newSocket.recv(1024)
            if len(recvDate)==0:
                print('the recvDate is:',recvDate)
                pass
            elif len(recvDate)!=0:
                print('recv[%s]:%s' % (str(destAddr), recvDate.decode()))
                break

    newSocket.close()
def main():
    serSocket = socket(AF_INET, SOCK_STREAM)
    serSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR  , 1)
    localAddr = ('127.0.0.1', 8080)
    serSocket.bind(localAddr)
    serSocket.listen(5)
    try:
        while True:
            print('-----主进程，%s:%s，等待新客户端的到来------\n'%localAddr)
            newSocket,destAddr = serSocket.accept()
            print('-----主进程，，接下来创建一个新的进程负责数据处理[%s]-----\n'%str(destAddr))
            client = Thread(target=dealWithClient, args=(newSocket,destAddr))
            client.start()
            #因为线程中共享这个套接字，如果关闭了会导致这个套接字不可用，
            #但是此时在线程中这个套接字可能还在收数据，因此不能关闭
            #newSocket.close()
    finally:
        serSocket.close()
if __name__ == '__main__':
    main()
