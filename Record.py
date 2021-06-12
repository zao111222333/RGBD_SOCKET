#! /usr/bin/python3
import time
import os
from multiprocessing import Queue
from typing import get_origin
from VIDEO_FORM import VIDEO_CONFI
from SOCKET import SOCKET_CLIENT_INIT, SEND_VIDEO
from RGBD_SENDER import RGBD_CAP,RGBD_INIT
from threading import Thread
import numpy as np

def PutIMG():
    global rgbd_queue,rgbd_confi
    color_confi = VIDEO_CONFI(shape=(480,640,3),
                    dWidth=8,
                    dType='np.uint8',
                    fps=24)
    
    depth_confi = VIDEO_CONFI(shape=(480,640,1),
                    dWidth=8,
                    dType='np.uint8',
                    fps=24)
    color_stream, depth_stream = RGBD_INIT()
    while 1:   

        image_RGBD = RGBD_CAP(color_stream, depth_stream, color_confi, depth_confi,rgbd_confi)
        try:
            rgbd_queue.put(image_RGBD,block=True,timeout=2)
        except:
            print('消息队列已经满，现在有消息数量：%s'%(rgbd_queue.qsize()))
            print('~~~~~~~~~~~~~~~~~~~~~~')

def SentIMG():
    global rgbd_queue,rgbd_confi
    period = 1.0/rgbd_confi.fps
    # outdir = 'out_'+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    # print (outdir)
    # os.makedirs(outdir)
    i=0
    while 1:
        time_before = time.perf_counter()
        
        #image_RGBD = (np.ones(rgbd_confi.shape,dtype=eval(rgbd_confi.dType ))).tobytes()
        #print (len(image_RGBD))
        try:
            image_RGBD = rgbd_queue.get(block=True,timeout=2)
            image_color = image_RGBD[:,:,0:3]
            image_depth = image_RGBD[:,:,3]
            import cv2
            cv2.imwrite('out/image_color'+'%05d' % i+'.jpg', image_color)
            cv2.imwrite('out/image_depth'+'%05d' % i+'.jpg', image_depth)
        except:
            print('rgbd_queue is EMPTY')
            pass
        #SEND_IMG(conn,confi,img)

        if i>=500:
            break
        i=i+1

        while (time.perf_counter() - time_before) < period:
            time.sleep(0.001) 
     


if __name__ == '__main__':    
    global rgbd_confi,rgbd_queue

    rgbd_confi = VIDEO_CONFI(shape=(480,640,4),
                dWidth=8,
                dType='np.uint8',
                fps=24)

    rgbd_queue = Queue(3)

    putImg = Thread(target=PutIMG)
    putImg.start()

    sentImg = Thread(target=SentIMG)
    sentImg.start()
