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


while 1:
    if (not(os.path.exists('1.token'))):
        file=open('1.token',"a")
        file.close()
        print ('[SENT]')
        print ('(480, 640, 4)')
     