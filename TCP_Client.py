# -*- coding:utf-8 -*-
# 客户端
from socket import *
import time
import sys

# 奇偶性判断
def parityCheck(num):
    if num % 2 == 1:
        return 1
    elif num %2 == 0:
        return 0

def getDouble(num):
    return num*2

def checkSize10(num):
    if num > 10:
        return 1
    else:
        return 0

if __name__=='__main__':
    serverIp = "127.0.0.1"#input("请输入服务器的ip:")
    connNum = 3#input("请输入要链接服务器的次数(例如1000):")
    g_socketList = []
    for i in range(int(connNum)):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((serverIp, 8080))
        g_socketList.append((i,s))
        # print(i)

    try:
        while True:
            for i,s in g_socketList:
                time.sleep(0.5)
                msg = s.recv(1024)
                msg=str(msg)
                print("port_id:%d get the message:%s" % (i, msg))
                strNum=msg[msg.find('caculate:')+(len('caculate:')):-1]
                randList=[]
                dealNum=0

                # 提取数据
                for t in strNum:
                    if t.isdigit():
                        dealNum*=10
                        dealNum+=int(t)
                print("--%d--get"%(dealNum))

                # 数据处理
                retTemp=dealNum,parityCheck(dealNum),getDouble(dealNum),checkSize10(dealNum)
                temp = bytes(str(retTemp).encode())
                print("--%s--send:\n" %(temp))
                s.send(temp)

    except ConnectionAbortedError as err:
        print("{0}".format(err))
    except :
        print("Unexpected error:", sys.exc_info()[0])
