import time # 为了获取当前时间
from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(2.0) # 设置套接字超时时间为 1 秒
for i in range(1, 11):
    # 发送的报文为“Ping 序号 当前时间”
    # 这里的时间使用了 python 的格式化时间方法
    message = 'Ping ' + str(i) + ' ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        startTime = time.perf_counter() # 开始时间，以微秒记
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        endTime = time.perf_counter() # 结束时间
        delay = (endTime-startTime) * 1000 # 延迟时间为结束时间和开始时间的差，乘上 1000，以毫秒记
        print('%s  延迟：%f ms\n' % (modifiedMessage.decode(), delay))
    # 如果超时，则打印“请求超时！”
    except IOError:
        print('请求超时！\n')