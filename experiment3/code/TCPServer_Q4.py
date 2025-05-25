import socket
import random
import struct
from socket import *

def get_random_buffer_size():
    return random.randint(0, 5) + 1

def receive_all(connectionSocket, n):
    data = b''  # Start with an empty bytes object
    while len(data) < n:
        # Receive data. Try to receive the remaining bytes needed (n - len(data)).
        packet = connectionSocket.recv(n - len(data))
        if not packet:
            # If recv returns an empty bytes object, the client has closed the connection.
            return b'' # Return empty bytes to signal connection closed
        data += packet # Append the received bytes to our data buffer
    return data # Return the accumulated bytes once exactly n bytes are received
        
if __name__ == '__main__':
    # 服务器端口号
    serverPort = 12000
    # 创建服务器套接字，使用IPv4协议，TCP协议
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # 设置端口重用，以便服务能迅速重启
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # 绑定端口号和套接字
    serverSocket.bind(('', serverPort))
    # 开启监听
    serverSocket.listen(1)
    print('The server is ready to receive')
    while True:
        # 等待接受客户端的连接
        connectionSocket, addr = serverSocket.accept()
        # 设置mes编号
        mes_idx = 1
        # 不断处理客户端的请求
        # while True:
        #     # 接受客户端的数据
        #     sentence = connectionSocket.recv(1024).decode('utf-8')
        #     # 输出客户端发来的数据
        #     print('server get mes{}: {}'.format(mes_idx, sentence.replace('\0', '')))
        #     # 若以\0为结束，则停止监听
        #     if sentence.endswith('\0'):
        #         print('server end listening from client')
        #         break
        #     mes_idx += 1
        while True:
                # --- Step 1: Receive the 4-byte length prefix ---
                # We must read exactly 4 bytes to get the length indicator
            # print("Attempting to receive length prefix (4 bytes)...")
                length_prefix = receive_all(connectionSocket, 4)

                if not length_prefix:
                    # receive_all returned empty bytes, meaning the client closed the connection gracefully
                # print('server detected client closed connection.')
                    break # Exit the inner loop for this client

                # --- Step 2: Unpack the length ---
                # Use struct.unpack to convert the 4 bytes back into an integer
                # '!I' matches the format used by struct.pack on the client
                # unpack returns a tuple, so we take the first element [0]
                message_length = struct.unpack('!I', length_prefix)[0]
            # print(f"Received length prefix indicating message length: {message_length} bytes.")

                if message_length <= 0:
                     # Optional: Handle zero or negative length as potentially invalid data
                # print(f"Received invalid message length: {message_length}. Closing connection.")
                     break


                # --- Step 3: Receive the actual message data ---
                # Now that we know the length, read exactly that many bytes
            # print(f"Attempting to receive message data ({message_length} bytes)...")
                sentence_bytes = receive_all(connectionSocket, message_length)
                
                if not sentence_bytes:
                     # This case should theoretically not happen if length_prefix was received
                     # but it's a safeguard against unexpected mid-message disconnects.
                     print('server failed to receive full message body after getting length.')
                     break # Exit the inner loop

                # --- Step 4: Decode and process the complete message ---
                sentence = sentence_bytes.decode('utf-8') # Decode the bytes back to a string

                # Output the complete message received
                # The server's mes_idx now correctly counts the original messages
                print(f'server got mes{mes_idx}: {sentence}')

                mes_idx += 1 # Increment message index for the next complete message


        # 连接关闭
        connectionSocket.close()
