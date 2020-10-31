import socket
import threading
import sys



#set up variable
localIP= "127.0.0.1"
localPort= int (sys.argv[1])
bufferSize= 1024
msgFromServer= "Hello UDP Client"
FORMAT= "utf-8"
bytesToSend= str.encode(msgFromServer)
ADDR1= (localIP, localPort)
ADDR2= (localIP, localPort+1)
# Create a datagram socket and bind it to address and ip
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPServerSocket.bind(ADDR1)
print("[UDP server is running]")
TCPServerSocket.bind(ADDR2)

login_stat= False
login_status= {"client port": False}
whoami_name= ""
whoami_dic= {"client port": "name"}

import sqlite3
#define connection and cursor
sql_connection= sqlite3.connect("assignment1.db",check_same_thread=False)
my_cursor= sql_connection.cursor()

my_cursor.execute(""" CREATE TABLE IF NOT EXISTS User(
                Username text Primary Key, 
                Email text,
                Password text)""")
sql_connection.commit()
#prints out the table
my_cursor.execute("SELECT * FROM User")
print("very begining")

list_user= list(my_cursor.fetchall())
print("Name Email")
for sub_list in list_user:
    print(sub_list[0]+ "  "+ sub_list[2])
sql_connection.close()




# handle incoming UDP message 
def UDP_handle():
    global login_stat
    global whoami_name
    UDP_msg_raw = UDPServerSocket.recvfrom(bufferSize)
    UDP_clientMsg = UDP_msg_raw[0].decode(FORMAT)
    UDP_address = UDP_msg_raw[1]
    UDP_clientMsg_list= UDP_clientMsg.split()

    if (len(UDP_clientMsg_list)== 4 and UDP_clientMsg_list[0]== 'register' ):
        # create data entry in sqlite
        sql_connection= sqlite3.connect("assignment1.db",check_same_thread=False)
        my_cursor= sql_connection.cursor()
        
        sql= "INSERT INTO User VALUES ('" + UDP_clientMsg_list[1] + "','"+ UDP_clientMsg_list[2] + "','"+ UDP_clientMsg_list[3]+ "')"
        print(sql)
        my_cursor.execute(sql)
        print("sql execute")
        sql_connection.commit()
        print("sql commit")
        sql_connection.close()
        print("sql close")
        UDPServerSocket.sendto("Register successfully".encode(FORMAT), UDP_address)

    elif (len(UDP_clientMsg_list) < 4 and UDP_clientMsg_list[0]== 'register' ):
        UDPServerSocket.sendto("Usage: register <username> <email> <password>".encode(FORMAT), UDP_address)
    elif UDP_clientMsg_list[0]==  "whoami": 
        #connect to server and find name
        if UDP_address in login_status and login_status.get(UDP_address):
            name= whoami_dic.get(UDP_address)
            UDPServerSocket.sendto(name.encode(FORMAT), UDP_address)
        else: 
            UDPServerSocket.sendto("Please login firs.".encode(FORMAT), UDP_address)
   

# running in parrell in each client, handle each client
def TCP_handle():
    global login_stat
    global whoami_name
    conn, addr = TCPServerSocket.accept() 
    #set up TCP connection in a given thread
    print(f"[NEW CONNECTION] {addr} connected.")
    bytesAddressPair = conn.recvfrom(bufferSize)
    clientMsg = bytesAddressPair[0].decode(FORMAT)
    clientMsg_list= clientMsg.split()
    address = bytesAddressPair[1]
    connected= True
    print("handle client")
    print(clientMsg_list)

    while connected: 
        #Login  
        if (len(clientMsg_list)== 3 and clientMsg_list[0]== 'login'):
            input_username= clientMsg_list[1]
            input_password= clientMsg_list[2]
            # find data from sql
            sql_conn= sqlite3.connect("assignment1.db", check_same_thread=False)
            cursor= sql_conn.cursor()
            findID= "select Password FROM User where Username = '" + input_username + "'" 
            cursor.execute(findID)
            DB_password= cursor.fetchone()
            DB_password= ''.join(DB_password)
            sql_conn.close()
            
            if(input_password== DB_password): #login successful
                #if the address exist and login status is true
                if addr in login_status and login_status.get(addr):
                    conn.sendall("Please logout first.".encode(FORMAT))
                    #receive input from the client again
                    bytesAddressPair = conn.recvfrom(bufferSize)
                    clientMsg = bytesAddressPair[0].decode(FORMAT)
                    clientMsg_list= clientMsg.split()
                else:
                    login_status[addr]= True
                    whoami_dic[addr]= input_username
                    welcome= "Welcome, "+input_username
                    conn.sendall(welcome.encode(FORMAT))
                    #receive input from the client again
                    bytesAddressPair = conn.recvfrom(bufferSize)
                    clientMsg = bytesAddressPair[0].decode(FORMAT)
                    clientMsg_list= clientMsg.split()
            # if password doesnt match
            else:
                conn.sendall("Login failed.".encode(FORMAT))
                #receive input from the client again
                bytesAddressPair = conn.recvfrom(bufferSize)
                clientMsg = bytesAddressPair[0].decode(FORMAT)
                clientMsg_list= clientMsg.split()
        
        elif (len(clientMsg_list)< 2 and clientMsg_list[0]== 'login'): #login info not complete 
            conn.sendall("Usage: login <username> <password>".encode(FORMAT))
            #receive input from the client again
            bytesAddressPair = conn.recvfrom(bufferSize)
            clientMsg = bytesAddressPair[0].decode(FORMAT)
            clientMsg_list= clientMsg.split()
        
        #logout 
        elif(clientMsg_list[0]== 'logout'):
            if addr in login_status and login_status.get(addr):
                login_status.pop(addr)
                whoami_dic.pop(addr)
                messgage= "Bye, "+input_username
                conn.sendall(messgage.encode(FORMAT))
                #receive input from the client again
                bytesAddressPair = conn.recvfrom(bufferSize)
                clientMsg = bytesAddressPair[0].decode(FORMAT)
                clientMsg_list= clientMsg.split()
            else: 
                messgage= "Please login first."
                conn.sendall(messgage.encode(FORMAT))
                #receive input from the client again
                bytesAddressPair = conn.recvfrom(bufferSize)
                clientMsg = bytesAddressPair[0].decode(FORMAT)
                clientMsg_list= clientMsg.split()

        #list-user
        elif (clientMsg_list[0]== 'list-user'):
            # find users from sql database
            sql_conn= sqlite3.connect("assignment1.db", check_same_thread=False)
            cursor= sql_conn.cursor()
            cursor.execute("SELECT * FROM User")
            list_user= list(cursor.fetchall())
            # conn.sendall("Name Email".encode(FORMAT))
            for sub_list in list_user:
                useremail= sub_list[0]+ "  "+ sub_list[1] +"\n"
                conn.sendall(useremail.encode(FORMAT))

            sql_conn.close()
            #receive input from the client again
            bytesAddressPair = conn.recvfrom(bufferSize)
            clientMsg = bytesAddressPair[0].decode(FORMAT)
            clientMsg_list= clientMsg.split()
        #exit
        elif (clientMsg_list[0]== 'exit'):
            print("exit")
            conn.close()
            break

        
   
    conn.close() 


# start function starts the sever and opens up multithreading
def start_threading():
    TCPServerSocket.listen()
    print(f"[TCP Server is listening]")
    while True: 
        # block wait for new connect to the server, 
        # when the new connection occur, pass that to handle_client 
        thread= threading.Thread(target= TCP_handle) 
        thread.start() 
        UDP_handle()
        # one thread represents one  client  
        print(f"[Active Connections]{threading.activeCount()-1}")

while(True):
    start_threading()
    
    



    



