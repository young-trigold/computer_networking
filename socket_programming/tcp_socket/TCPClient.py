from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input('输入一个全是小写的句子：')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('来自服务器的消息：', modifiedSentence.decode())
clientSocket.close()