import socket
from _thread import *
import sys

server = "192.168.15.7"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object connecting to the server

try:
    s.bind((server, port))
except socket.error as e:  # Catch any errors
    str(e)

# Listen for at least 2 and at most 8 players
s.listen(2)
print("Waiting for a connection, Server Started")

def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)
            conn.sendall(str.encode(reply))
        except:
            break
    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()  # Accept a connection from a client
    print("Connected to: ", addr)

    # Start a new thread for each client
    start_new_thread(threaded_client, (conn,))




    
