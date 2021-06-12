#! /bin/python3

# socket
import socket
import struct

def SOCKET_INIT(TAG_IP,TAG_PORT)
    state = 0
    try:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect((TAG_IP, TAG_PORT))
    except socket.error as msg:
        print (msg)
        state = 1
        return state
        
    b = sk.recv(1024) 
    bs = str(b, encoding = "utf8")
    print (bs)

if __name__ == '__main__':
    SOCKET_INIT