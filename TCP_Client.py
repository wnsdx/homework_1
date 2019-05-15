# -*- coding:utf-8 -*-
# 客户端
from socket import *
import random
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
                # print("%d get the message:%s"%(i,msg))
                # print(type(msg))
                msg=str(msg)
                strList=msg[msg.find('caculate:')+len('caculate:'):]
                # print(type(strList))
                randList=[]
                old=0
                retList=[]

                # 提取数据
                for t in strList:
                    if t.isdigit():
                        old*=10
                        old+=int(t)
                    elif t==',' or t==']':
                        randList.append(old)
                        old=0
                print("--%d--get"%(i),end='')
                print(randList)

                # 数据处理
                for listTemp in randList:
                    retTemp=listTemp,parityCheck(listTemp),getDouble(listTemp),checkSize10(listTemp)
                    retList.append(str(retTemp))
                    # print(retTemp)
                    temp = bytes(str(retList).encode())
                # print("--%d--send:" % (i))
                s.send(temp)
                # s.send(bytes(random.randint(0, 100)))
            break
    except ConnectionAbortedError as err:
        print("{0}".format(err))
    except :
        print("Unexpected error:", sys.exc_info()[0])
