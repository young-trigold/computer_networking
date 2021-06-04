from socket import *

serverName = 'localhost' # 服务器为本地主机

serverPort = 12000 # 端口号

clientSocket = socket(AF_INET, SOCK_DGRAM) # 新建 UDP 客户套接字

message = input('输入一个全是小写的句子：')

clientSocket.sendto(message.encode(), (serverName, serverPort)) # 发送消息

rcvMessage, serverAddress = clientSocket.recvfrom(2048)

print(rcvMessage.decode ())

clientSocket.close()