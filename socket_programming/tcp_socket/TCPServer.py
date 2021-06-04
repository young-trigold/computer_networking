from socket import *

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('', 12000))

serverSocket.listen(1)

print('服务器已经准备好接收了！')

while True:
    connectionSocket, addr = serverSocket.accept()
    sentenceInput = connectionSocket.recv(1024).decode()
    sentenceOutput = sentenceInput.upper()
    connectionSocket.send(sentenceOutput.encode())
    connectionSocket.close()