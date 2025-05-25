from socket import *

if __name__ == '__main__':
    # 服务器端口号
    # serverPort = ...
    serverPort = 12000
    # 创建服务器套接字，使用IPv4协议，UDP协议
    # serverSocket = ...
    # AF_INET -- IPv4, SOCK_DGRAM -- UDP protocal
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    # 绑定端口号和套接字
    # bind
    serverSocket.bind(('', serverPort))
    
    # 提示信息
    print("The server is ready to receive")
    # 进程一直运行，等待分组到达
    while (True):
        # 接收报文
        # 1024是一个常见的缓冲区大小
        msg, caddr = serverSocket.recvfrom(1024)        
        # 处理
        # .decode() converts bytes to string
        # .upper() to uppercase
        # .encode() string to byte (UTF-8) by default
        mmsg = msg.decode().upper().encode()
        
        # 发送报文
        # sendto(data, addr_of_revipient) - Send the processed data
        serverSocket.sendto(mmsg, caddr) 
    # err_handling