import random # 导入 random 包来生成随机的丢失的分组
from socket import * 
# 创建一个 UDP 套接字
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 12000))
print('服务器已启动！\n')
while True:
    # 生成 0 到 10 的随机数字
    rand = random.randint(0, 10)
    # 接收客户分组和客户地址
    message, address = serverSocket.recvfrom(1024)
    print(message.decode() + '\n')
    # 将来自客户的报文大写
    message = message.upper()
    # 随机生成的整数小于 4，则不发送报文
    if rand < 4:
        continue
    serverSocket.sendto(message, address)