#import socket module
from socket import *
import threading

def handle_client(connectionSocket, addr):
    try:
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        message =  connectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])

        outputdata = f.read()

        #Send one HTTP header line into socket
        connectionSocket.send('HTTP/1.x 200 OK\r\n'.encode())
        connectionSocket.send('Content-Type: text/html\r\n\r\n'.encode())
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        connectionSocket.send('404 Page Not Found\r\n'.encode())
        connectionSocket.send('Content-Type: text/html\r\n\r\n'.encode())
        connectionSocket.send('<html><body><h1>404 Page Not Found</h1></body></html>'.encode())

        #Close client socket
        connectionSocket.close()

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
serverSocket.bind(('127.0.0.1', 12345))
serverSocket.listen(1)
print("Server is listening...")
while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr =  serverSocket.accept() 
    
    thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
    thread.start()

serverSocket.close()