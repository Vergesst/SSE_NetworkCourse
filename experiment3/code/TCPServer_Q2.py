from socket import *

if __name__ == '__main__':
    # 服务器端口号
    serverPort = 12000
    # 创建服务器套接字，使用IPv4协议，TCP协议
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # 绑定端口号和套接字
    serverSocket.bind(('', serverPort))
    # 开启监听
    # listen() - listen for incoming connections rather than port
    serverSocket.listen(1)
    print('The server is ready to receive')
    while (True):
        # 等待接受客户端的连接
        connectionSocket, addr = serverSocket.accept()
        # 接受客户端的数据
        sentence = connectionSocket.recv(1024)
        # 数据处理
        capitalizedSentence = sentence.lower()
        # 把结果发送回客户端
        connectionSocket.send(capitalizedSentence)
        # 连接关闭
        if(input() == "exit" or input() == "quit"):
            print("Server is shutting down...")
            break
        
    serverSocket.close()
