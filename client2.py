#! /usr/bin/env python3
import socket
import sys

bufferSize= 1024
FORMAT= "utf-8"
login= False
my_name= ""
localPort= int (sys.argv[2])
IP= sys.argv[1]

UDPserverAddressPort= ('127.0.0.1', 5201)
TCPserverAddressPort= ('127.0.0.1', 5202)
# Create UDP and TCP socket at client side
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

TCPClientSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPClientSocket.connect(TCPserverAddressPort)
# Send to server using created UDP socket
msgFromClient= "Hello UDP Server"
bytesToSend= str.encode(msgFromClient)

client_tcp_port=""
while (True): 
    #send user input to server
    user_input = input("please enter:") 
    command= user_input.split()
    if (command[0]== "register"):
        UDPClientSocket.sendto(user_input.encode(FORMAT), UDPserverAddressPort)
        #receive message from the server
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = msgFromServer[0].decode(FORMAT)
        print("UDP: login response from server")
        print(msg)
    elif (command[0]== "whoami"):
        UDPClientSocket.sendto(user_input.encode(FORMAT), UDPserverAddressPort)
        #receive message from the server
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = msgFromServer[0].decode(FORMAT)
        print(msg)
        
    elif(command[0]== "login"):
        TCPClientSocket.sendto(user_input.encode(FORMAT), TCPserverAddressPort)
        #receive message from the server
        msgFromServer = TCPClientSocket.recvfrom(bufferSize)
        msg = msgFromServer[0].decode(FORMAT)
        print(msg)
    elif(command[0]== "list-user"):
        TCPClientSocket.sendto(user_input.encode(FORMAT), TCPserverAddressPort)
        #receive message from the server
        msgFromServer = TCPClientSocket.recvfrom(bufferSize)
        msg = msgFromServer[0].decode(FORMAT)
        print(msg)

        #receive message from the server
        msgFromServer = TCPClientSocket.recvfrom(bufferSize)
        msg = msgFromServer[0].decode(FORMAT)
        print(msg)

    elif(command[0]== "logout"):
        TCPClientSocket.sendto(user_input.encode(FORMAT), TCPserverAddressPort)
        #receive message from the server
        msgFromServer = TCPClientSocket.recvfrom(bufferSize)
        msg = msgFromServer[0].decode(FORMAT)
        print(msg) 
    elif(command[0]== "exit"):
        TCPClientSocket.sendto(user_input.encode(FORMAT), TCPserverAddressPort)
        break
       
    
        
    else: 
        user_input = input("please enter again:") 
        command= user_input.split()
        msgFromServer = TCPClientSocket.recvfrom(bufferSize)
        msg = msgFromServer[0].decode(FORMAT)
        print(msg)


    