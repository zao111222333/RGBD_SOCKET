from openni import openni2
from openni import _openni2 as c_api
import numpy as np
import cv2

import sys

openni2.initialize('./Orbbec/Redist')
dev = openni2.Device.open_any()

color_stream = dev.create_color_stream()
color_stream.start()
color_frame = color_stream.read_frame()
image_color = np.frombuffer(color_frame.get_buffer_as_uint8(), dtype=np.uint8).reshape([480,640,3])
image_color = cv2.cvtColor(image_color,cv2.COLOR_BGR2RGB)
cv2.imwrite('image_color.jpg', image_color)

depth_stream = dev.create_depth_stream()
depth_stream.start()
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM, resolutionX = 640, resolutionY = 480, fps = 30))
depth_frame = depth_stream.read_frame()
image_depth = np.frombuffer(depth_frame.get_buffer_as_uint8(), dtype=np.uint16).reshape([480,640,1])

nonzero_index = np.nonzero(image_depth)
if nonzero_index[0].size !=0 :
    minval = np.min(image_depth[nonzero_index])
    maxval = np.max(image_depth[nonzero_index])
    image_depth = 255*((image_depth - minval) / (maxval-minval))
cv2.imwrite('image_depth.jpg', image_depth)
