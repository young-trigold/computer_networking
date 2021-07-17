from socket import * # 导入 socket 模块
import sys # 为了退出服务器程序
serverSocket = socket(AF_INET, SOCK_STREAM)
# 准备一个欢迎套接字
# 开始补全
# 结束补全
statusLineFor200 = 'HTTP/1.1 200 OK\n' # 构造 HTTP 响应报文中请求成功状态行
statusLineFor404 = # 开始补全 # 结束补全 # 构造 HTTP 响应报文中找不到请求对象状态行
newLine = '\n' # 空行
while True:
    print('服务器已启动！\n')
    connectionSocket, addr = # 开始补全 # 结束补全 # 建立连接
    try:
        message = # 开始补全 # 结束补全
        filename = message.split()[1] # 使用空格将 HTTP 请求报文分隔，并提取出请求对象 URL
        print('请求行：' + message.split('\n')[0] + '\n') # 打印出 HTTP 请求报文中的请求行
        content = open(filename[1:]).read() # 读取文件，构造 HTTP 响应报文实体体
        outputdata = # 开始补全 # 结束补全 # 构造 HTTP 响应报文
        print('HTTP响应报文：' + outputdata + '\n')
        connectionSocket.send(outputdata.encode())
        connectionSocket.close()
        print('连接已关闭！\n')
    except IOError:
        notFound = statusLineFor404 + newLine + open('404.html').read() # 构造 HTTP 响应报文
        print('HTTP响应报文：' + notFound + '\n')
         # 开始补全 # 结束补全 # 发送 404 响应报文
        # 开始补全 # 结束补全 # 关闭连接
        print('连接已关闭！\n')
    serverSocket.close() # 关闭欢迎套接字
    print('服务器已关闭！\n')
    sys.exit() # 退出控制台