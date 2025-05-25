from socket import *

if __name__ == '__main__':
    # 服务器的IP地址或主机名
    serverName = '127.0.0.2'
    # 服务器端口号
    serverPort = 12000
    # 创建客户套接字，使用IPv4协议，TCP协议
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # 三次握手，建立TCP连接
    clientSocket.connect((serverName, serverPort))
    while True:
        # 输入任意字符串
        sentence = input('Input lowercase sentence (bye to quit): ')
        # 发送任意字符串
        clientSocket.send(sentence.encode('utf-8'))
        # 输入bye，结束运行
        if sentence == 'bye':
            print('client end')
            break
        # 接受任意字符串
        modifiedSentence = clientSocket.recv(1024)
        # 输出结果
        print('From Server:', modifiedSentence.decode('utf-8'))
    # 关闭socket
    socket.close()
