# import socket module
import os
from socket import *

if __name__ == '__main__':
    # 准备TCP套接字
    serverSocket = socket(AF_INET, SOCK_STREAM)
    PORT = 5000
    ADDRESS = "127.0.0.1"
    # 将TCP套接字绑定到指定端口
    serverSocket.bind((ADDRESS, PORT))
    # 设置最大连接数
    serverSocket.listen(1)

    while True:
        # 准备迎接客户端的连接
        print('Ready to serve...')
        # 接收到客户连接请求后，建立新的TCP连接套接字
        connectionSocket, addr = serverSocket.accept()
        try:
            # 获取客户发送的报文
            message = connectionSocket.recv(1024)
            # 获取客户端需要的文件名，根据html格式来进行切分
            filename = message.split()[1]
            filepath = f"./{filename[1:]}"
            
            # raise exception
            if not os.path.exists(filepath):
                raise IOError()
            # 读取文件
            f = open(filepath, 'rb')
            outputdata = f.read()
            print(f"Resolved filepath: {filepath}")
            f.close()
            # 发送http响应，记得要encode一下，因为网络传的是数据流，并在响应头设置好你设定的编码方式，比如utf-8
            # 200响应行
            response_line = "http/1.1 200 OK\r\n"
            # 响应头
            response_header = "Content-Type: text/html; charset=utf-8\r\n"
            # 空行
            empty = "\r\n"
            # 响应体
            response_body = outputdata
            # 拼接响应
            response = response_line + response_header + empty + response_body
            # 发送响应
            response = (response_line + response_header + empty).encode('utf-8') + response_body
            connectionSocket.sendall(response)
            # 关闭连接
            connectionSocket.close()
        except IOError:
            # 找不到这个文件，返回404
            # 读取404页面文件
            f = open('../404.html', 'rb')
            outputdata = f.read()
            # 404响应行
            response_line = "http/1.1 200 Not Found\r\n"
            # 响应头
            response_header = "Content-Type: text/html; charset=utf-8"
            # 空行
            empty = "\r\n"
            # 响应体
            response_body = outputdata
            # 拼接响应
            response = (response_line + response_header + empty).encode('utf-8') + response_body
            # 发送响应
            connectionSocket.sendall(response)
            # 关闭连接
            connectionSocket.close()
    serverSocket.close()
