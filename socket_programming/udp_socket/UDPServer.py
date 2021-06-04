from socket import *

serverPort = 12000 # 服务端端口

serverSocket = socket(AF_INET, SOCK_DGRAM) # 新建 UDP socket

serverSocket.bind(('', serverPort)) # 绑定 12000 端口

print('服务器已经准备好接收了！')

while True:
  rcvMessage, clientAddress = serverSocket.recvfrom(2048) # 储存客户端发来的信息
  
  sendMessage  = rcvMessage.decode().upper() # 大写信息

  serverSocket.sendto(sendMessage.encode(), clientAddress) # 发送信息