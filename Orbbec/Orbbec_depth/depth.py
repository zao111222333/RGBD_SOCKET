import cv2
import numpy as np
from openni import openni2
from openni import _openni2 as c_api
import time
import ctypes
from openni import openni2
redistPath = "Redist/" 
#redist就是sdk文件夹下，Windows下的Redist文件夹，里面是openni.ini等
openni2.initialize(redistPath) 
 
 
fps = 30      # frames per second
width = 640       # Width of image
height = 400      # height of image
 
 
dev = openni2.Device.open_any()
print(dev.get_device_info())
depth_stream = dev.create_depth_stream()
dev.set_image_registration_mode(True)
dev.set_depth_color_sync_enabled(True)
 
 
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM,
                                                   resolutionX=width,
                                                   resolutionY=height,
                                                   fps=fps))
depth_stream.start()
while True:
    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()
    img = np.ndarray((frame.height, frame.width), dtype=np.uint16,buffer=frame_data)
 
    cv2.imshow("Depth", cv2.equalizeHist(cv2.convertScaleAbs(img, alpha=255/img.max())))
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break
 
openni2.unload()
dev.close()
