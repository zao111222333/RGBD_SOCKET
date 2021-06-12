#! /bin/python3
import struct
import numpy as np

class VIDEO_CONFI:
    def __init__(self,shape=(640,480,3),dWidth=8,dType='uint8',fps=30):
        self.shape = shape
        self.dWidth = dWidth
        self.dType = dType
        self.fps = fps
        self.confi_struct = '<3II'+str(len(dType))+'sI'
    
    def __bytes__(self):
        # print(self.confi_struct)
        return struct.pack( str(self.confi_struct),
                           *self.shape,
                            self.dWidth,
                            str.encode(self.dType),
                            self.fps)
    def getFhead(self):
        return struct.pack('128si', str.encode(self.confi_struct), len(self.confi_struct))
    
    def fheadSize(self):
        return struct.calcsize('128si')

    def setStruct(self,fhead):
        # print(struct.unpack('128si',fhead))
        confi_struct, confi_struct_len = struct.unpack('128si',fhead)
        self.confi_struct = confi_struct[0:confi_struct_len].decode('UTF-8')
    
    def confiSize(self):
        return struct.calcsize(self.confi_struct)
    
    def setConfi(self,confi_bytes):
        # print(struct.unpack(self.confi_struct,confi_bytes))
        img_W, img_H, img_D, dWidth, dType, fps = struct.unpack(self.confi_struct,confi_bytes)
        self.shape = (img_W, img_H, img_D)
        self.dWidth = dWidth
        self.dType = dType.decode("utf-8")
        self.fps = fps

    def imgSize(self):
        return int(np.prod(self.shape)*self.dWidth/8)

    def equal(self,anotherConfi):
        return self.shape == anotherConfi.shape \
           and self.dWidth == anotherConfi.dWidth \
           and self.dType == anotherConfi.dType \
           and self.fps == anotherConfi.fps

if __name__ == '__main__':
    client_confi = VIDEO_CONFI(shape=(640,480,3),
                    dWidth=8,
                    dType='uint8',
                    fps=24)

    server_confi = VIDEO_CONFI()
    
    fhead = client_confi.getFhead()
    print('[CLIENT]fhead send   length:'+str(len(fhead)))
    print('[SERVER]fhead recive length:'+str(server_confi.fheadSize()))
    server_confi.setStruct(fhead)

    confi_bytes = bytes(client_confi)
    print('[CLIENT]confi send   length:'+str(len(confi_bytes)))
    print('[SERVER]confi recive length:'+str(server_confi.confiSize()))
    server_confi.setConfi(confi_bytes)

    print(server_confi.equal(client_confi))
