#! /bin/python3

# 多线程
from queue import Queue
# from multiprocessing import Process
from threading import Thread


# RGBD
from openni import openni2
from openni import _openni2 as c_api
import numpy as np
import cv2
from VIDEO_FORM import VIDEO_CONFI

import sys

# IMG_DIR = sys.argv[1]
# TAG_IP = sys.argv[2]
# TAG_PORT = int(sys.argv[3])
# d_len = 1024

def RGBD_INIT():
    ##### 1. 设备接入 #####
    openni2.initialize('./Orbbec/Redist')
    dev = openni2.Device.open_any()

    color_stream = dev.create_color_stream()
    depth_stream = dev.create_depth_stream()
    color_stream.start()
    depth_stream.start()
    depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM, resolutionX = 640, resolutionY = 480, fps = 30))
    
    return color_stream,depth_stream


def DEPTH_CAP(depth_stream,depth_queue,depth_shape):
    print(depth_shape)
    image_depth = np.zeros(depth_shape)
    depth_frame = depth_stream.read_frame()
    image_depth = np.frombuffer(depth_frame.get_buffer_as_uint8(), dtype=np.uint16).reshape(depth_shape)
    nonzero_index = np.nonzero(image_depth)
    if nonzero_index[0].size !=0 :
        minval = np.min(image_depth[nonzero_index])
        maxval = np.max(image_depth[nonzero_index])
        image_depth = 255*((image_depth - minval) / (maxval-minval))
    
    try:
        depth_queue.put(image_depth.tobytes(),block=True,timeout=2)
    except:
        print('消息队列已经满，现在有消息数量：%s'%(depth_queue.qsize()))
    print('~~~~~~~~~~~~~~~~~~~~~~')

def RGBD_CAP(color_stream, depth_stream, color_confi, depth_confi,rgbd_confi):
    image_depth = np.zeros(depth_confi.shape)
    depth_frame = depth_stream.read_frame()
    image_depth = np.frombuffer(depth_frame.get_buffer_as_uint8(), dtype=np.uint16).reshape(depth_confi.shape)
    nonzero_index = np.nonzero(image_depth)
    if nonzero_index[0].size !=0 :
        minval = np.min(image_depth[nonzero_index])
        maxval = np.max(image_depth[nonzero_index])
        image_depth = 255*((image_depth - minval) / (maxval-minval))

    image_color = np.zeros(color_confi.shape)
    color_frame = color_stream.read_frame()
    image_color = np.frombuffer(color_frame.get_buffer_as_uint8(), dtype=np.uint8).reshape(color_confi.shape)
    image_color = cv2.cvtColor(image_color,cv2.COLOR_BGR2RGB)
    #try:
    #    depth_queue.put(image_depth.tobytes(),block=True,timeout=2)
    #except:
    #    print('消息队列已经满，现在有消息数量：%s'%(depth_queue.qsize()))
    #print('~~~~~~~~~~~~~~~~~~~~~~')
    image_RGBB = np.concatenate((image_color,image_depth),axis=2) 
    print (image_RGBB.shape)
    return image_RGBB


def COLOR_CAP(color_stream,color_queue,color_shape):
    print(color_shape)
    image_color = np.zeros(color_shape)
    color_frame = color_stream.read_frame()
    image_color = np.frombuffer(color_frame.get_buffer_as_uint8(), dtype=np.uint8).reshape(color_shape)
    image_color = cv2.cvtColor(image_color,cv2.COLOR_BGR2RGB)
    try:
        color_queue.put(image_color.tobytes(),block=True,timeout=2)
    except:
        print('消息队列已经满，现在有消息数量：%s'%(color_queue.qsize()))
    print('~~~~~~~~~~~~~~~~~~~~~~')

def bytes2img(image_color_byte,confi):
    image_color = (np.frombuffer(image_color_byte, dtype=eval(confi.dType))).reshape(confi.shape)
    return image_color



if __name__ == '__main__':
    color_queue = Queue(5)
    depth_queue = Queue(5)
    color_confi = VIDEO_CONFI(shape=(480,640,3),
                    dWidth=8,
                    dType='np.uint8',
                    fps=24)
    
    depth_confi = VIDEO_CONFI(shape=(480,640,1),
                    dWidth=8,
                    dType='np.uint8',
                    fps=24)
    
    rgbd_confi = VIDEO_CONFI(shape=(480,640,4),
                dWidth=8,
                dType='np.uint8',
                fps=24)
    color_stream, depth_stream = RGBD_INIT()
    image_RGBD = RGBD_CAP(color_stream, depth_stream, color_confi, depth_confi,rgbd_confi)

    cv2.imwrite('image_color.jpg', image_RGBD[:,:,0:3])
    cv2.imwrite('image_depth.jpg', image_RGBD[:,:,3])



    #y = np.frombuffer(color_queue.get(), dtype=eval('np.'+color_confi.dtype))
    #recover = y.reshape(color_confi.shape)
    #re_image_color = cv2.cvtColor(recover,cv2.COLOR_BGR2RGB)