from snap7.util import *
from snap7.types import *
import snap7.client as c
import snap7
import qrcode


ip = '192.168.0.1'
rack =0
slot =0

# PLC.connect(ip,rack,slot)
plc = c.Client()

plc.connect(ip,rack,slot)   
flag = plc.get_connected()   
if flag == True:
    print("PLC Connect Success...........")
else: print("Connect Error")

class PLC():
    def __init__(self) :
        # self.plc = c.Client()

        pass


    def WriteMemory( byte, bit, datatype, value):
        global plc
        result = plc.read_area(Areas.MK, 0, byte, datatype)
        if datatype == S7WLBit:
            set_bool(result, 0, bit, value)
        elif datatype == S7WLByte or datatype == S7WLWord:
            set_int(result, 0, value)
        elif datatype == S7WLReal:
            set_real(result, 0, value)
        elif datatype == S7WLDWord:
            set_dword(result, 0, value)
        plc.write_area(Areas.MK, 0, byte, result)


    def ReadMemory( byte, bit, datatype):
        global plc
        result = plc.read_area(Areas.MK, 0, byte, datatype)
        if datatype == S7WLBit:
            return get_bool(result, 0, bit)
        elif datatype == S7WLByte or datatype == S7WLWord:
            return get_int(result, 0)
        elif datatype == S7WLReal:
            return get_real(result, 0)
        elif datatype == S7WLDWord:
            return get_dword(result, 0)
        else:
            return None