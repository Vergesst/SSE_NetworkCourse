from socket import *

if __name__ == "__main__":
    serverName = "127.0.0.1"
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    
    print("The server is ready to receive")
    connectionSocket, caddr = serverSocket.accept()
    while True:
        sentense = connectionSocket.recv(1024)
        capitalizedSentence = sentense.upper()
        if sentense == b"bye":
            print("Server is shutting down...")
            break
        connectionSocket.send(capitalizedSentence)
        