from socket import *
import random
import struct

# 准备好要发送的数据, ‘\0’，为结束
messages = ['Modern',
            'Chinese',
            'trace',
            'their',
            'origins',
            'to',
            'a',
            'cradle',
            'of',
            'civilization',
            'in',
            'the',
            'fertile',
            'basin',
            'of',
            'the',
            'Yellow',
            'River',
            'in',
            'the',
            'North',
            'China',
            'Plain',
            '\0']

# 本质上多次调用sendall后操作系统底层有可能会将数据包合并发送，比如第一次发送的数据是A，第二次是B
# 操作系统可能会将A和B合并成C（A+B）发送，这样子接收端就可能不知道这个数据C的边界在哪，如何分割回A和B
# 因此，为了更好的模拟实际场景，我们进一步得将数据分块发送

# original send function
# def split_send(clientSocket, mes: []):
#     l, n = 0, len(mes)
#     while l < n:
#         send_len = random.randint(0, n - l) + 1
#         clientSocket.sendall(mes[l:l + send_len])
#         l += send_len

def send_message(clientSocket, message):
    emsg = message.encode('UTF-8') # 将消息编码为字节
    msg_length = len(emsg) # 获取消息长度
    
    # Pack the message length (an integer) into a fixed-size bytes object (4 bytes)
    # '!I' format: ! means network byte order (big-endian), I means unsigned integer (4 bytes)
    length_prefix = struct.pack('!I', msg_length)

    # Send the 4-byte length prefix followed immediately by the message bytes
    # sendall ensures that all bytes from *this* call are eventually sent,
    # but the key is the prefix tells the receiver how many to read *next*.
    clientSocket.sendall(length_prefix + emsg)


if __name__ == '__main__':
    # 服务器的IP地址或主机名
    serverName = '127.0.0.1'
    # 服务器端口号
    serverPort = 12000
    # 创建客户套接字，使用IPv4协议，TCP协议
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # 三次握手，建立TCP连接
    clientSocket.connect((serverName, serverPort))
    # 设置mes编号
    mes_idx = 1
    for mes in messages:
        # 输出发送的消息
        print('client sent mes{}: {}'.format(mes_idx, mes))
        # 发送mes
        # split_send(clientSocket, mes.encode('UTF-8'))
        send_message(clientSocket, mes)
        # 消息标号加一
        mes_idx += 1
    # 关闭socket
    clientSocket.send('\0'.encode('UTF-8'))
    clientSocket.close()
