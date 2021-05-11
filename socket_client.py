#! /bin/python3
# -*- coding=utf-8 -*-

import socket
import os
import sys
import struct
import time

frequency = 30  # Hz
period = 1.0/frequency

def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('10.20.70.181', 6666))
    except socket.error as msg:
        print (msg)
        sys.exit(1)
    
    #  bytes to str
    b = s.recv(1024) 
    bs = str(b, encoding = "utf8")
    print (bs)
    i=0
    while 1:
        time_before = time.perf_counter()
        print(i)
        i=i+1
        filepath = "/home/pi/RGBD_CLIENT/img/img0000_color.jpeg"
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            basename_byte = str.encode(os.path.basename(filepath))
            fhead = struct.pack('128sl', basename_byte, os.stat(filepath).st_size)
            s.send(fhead)
            # print ('client filepath: {0}'.format(filepath))

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    # print ('{0} file send over...'.format(filepath))
                    break
                s.send(data)
        #s.close()
        while (time.perf_counter() - time_before) < period:
            time.sleep(0.001)  # precision here


if __name__ == '__main__':
    socket_client()