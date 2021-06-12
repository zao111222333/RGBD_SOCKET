#! /usr/bin/python3
import socket
import struct
import time
import numpy as np
from VIDEO_FORM import VIDEO_CONFI

def SOCKET_CLIENT_INIT(TAG_IP, TAG_PORT):
    state = 1
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((TAG_IP, TAG_PORT))
    except socket.error as msg:
        print (msg)
        state = 0
    return state,conn

def SOCKET_SERVER_INIT(IP, PORT):
    state = 1
    try:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sk.bind((IP, PORT))
        sk.listen(10)
    except socket.error as msg:
        print (msg)
        state = 0
        return state, sk
    print ('[BUILD] Waiting connection...')
    return state, sk

def RECV_HI(conn):
    hi = conn.recv(1024) 
    hi_str = str(hi, encoding = "utf8")
    print(hi_str)

def SEND_HI(conn, addr):
    print ('Accept new connection from {0}'.format(addr))
    hi = str.encode("Hi, Welcome to the server!")
    conn.send(hi)

def SEND_CONFI(conn,confi):
    fhead = confi.getFhead()
    conn.send(fhead)

    config_bytes = bytes(confi)
    conn.send(config_bytes)

def RECIVE_CONFI(conn):
    confi = VIDEO_CONFI()
    fhead = conn.recv(confi.fheadSize())
    confi.setStruct(fhead)
    confi_bytes = conn.recv(confi.confiSize())
    confi.setConfi(confi_bytes)
    return confi

def SEND_AND_VERIFY_CONFI(conn,confi):
    token = b'verifyed'
    while 1:
        SEND_CONFI(conn,confi)
        confi_ = RECIVE_CONFI(conn)
        if confi.equal(confi_):
            conn.send(token)
            break
        time.sleep(1)
    print('[CLIENT] Video Configure is Verified!')

def RECV_AND_VERIFY_CONFI(conn):
    token = b'verifyed'
    while 1:
        confi = RECIVE_CONFI(conn)
        SEND_CONFI(conn,confi)
        token_ = conn.recv(len(token))
        if token_ == token:
            break
        time.sleep(1)
    print('[SERVER] Video Configure is Verified!')
    return confi

def SEND_IMG(conn,confi,img):
    print(len(img))
    conn.send(img)

def RECV_IMG(conn,confi):
    print(confi.imgSize())
    img = conn.recv(confi.imgSize())
    return img

def RECV_VIDEO(conn, addr, video_queue):
    SEND_HI(conn, addr)
    server_confi = RECV_AND_VERIFY_CONFI(conn)
    while 1:
        img = RECV_IMG(conn,server_confi)
        print(img[1])
        try:
            video_queue.put(img,block=True,timeout=2)
        except:
            print('video_queue is FULL')
            pass
        time.sleep(0.01)


def SEND_VIDEO(conn,confi,video_queue):
    RECV_HI(conn)
    SEND_AND_VERIFY_CONFI(conn,confi)
    
    period = 1.0/confi.fps
    while 1:
        time_before = time.perf_counter()
        
        img = (np.ones(confi.shape,dtype=eval(confi.dType ))).tobytes()
        print (len(img))
        try:
            img = video_queue.get(block=True,timeout=2)
        except:
            print('video_queue is EMPTY')
            pass
        SEND_IMG(conn,confi,img)
        while (time.perf_counter() - time_before) < period:
            time.sleep(0.001) 
        

    #server_confi = RECIVE_CONFI(conn)
    #print(confi.equal(server_confi))