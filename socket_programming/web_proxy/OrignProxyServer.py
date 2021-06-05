from socket import *
import sys
if len(sys.argv) <= 1:
    print('使用方法："python ProxyServer.py server_ip"\n[server_ip : 这是你代理服务器的IP地址]')
    sys.exit(2)
# 创建一个服务器 socket，将它绑定到一个端口并开始监听
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# 开始补全 
# 结束补全
while 1:
    # 开始接收来自客户的数据
    print('服务器已启动！\n')
    tcpCliSock, addr = tcpSerSock.accept()
    print('接收到一个连接，来自于：', addr)
    message = # 开始补全 # 结束补全
    print(message)
    # 从 message 中提取出文件名
    print(message.split()[1])
    filename = message.split()[1].partition('/')[2]
    print(filename)
    fileExist = 'false'
    filetouse = '/' + filename
    print(filetouse)
    try:
        # 检查缓存中是否存在
        f = open(filetouse[1:], 'r')
        outputdata = f.readlines()
        fileExist = 'true'
        # 代理服务器找到缓存并生成一个响应报文
        tcpCliSock.send('HTTP/1.1 200 OK\n')
        tcpCliSock.send('Content-Type: text/html\n')
        # 开始补全
        # 结束补全
        print('从缓存中读取')
    # 处理缓存中没有文件的异常
    except IOError:
        if fileExist == 'false':
            # 在代理服务器上创建一个套接字
            c = # 开始补全 # 结束补全
            hostn= filename.replace('www.', '', 1)
            print(hostn)
            try:
                # 连接套接字到 80 端口
                # 开始补全
                # 结束补全
                # 创建一个临时文件在 socket 上，并询问 80 端口客户请求的文件
                fileobj = c.makefile('r', 0)
                fileobj.write('GET ' + 'http://' + filename + 'HTTP/1.0\n\n')
                # 将响应写进缓存
                # 开始补全
                # 结束补全
                # 在缓存中为请求的文件创建一个新的文件
                # 并发送在缓存的响应给客户套接字并且在缓存中找出对应的文件
                tempFile = open('./' + filename, 'wb')
                # 开始补全
                # 结束补全
            except IOError:
                # 找不到请求文件的 HTTP 响应报文
                # 开始补全
                # 结束补全
        # 关闭客户和服务器的套接字
        tcpCliSock.close()
    # 开始补全
    # 结束补全
