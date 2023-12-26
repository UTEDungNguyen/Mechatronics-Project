from snap7.util import *
from snap7.types import *
import snap7.client as c
import snap7
import time

'''
Areas = ADict({
    'PE': 0x81,
    'PA': 0x82,
    'MK': 0x83,
    'DB': 0x84,
    'CT': 0x1C,
    'TM': 0x1D, 
})
'''


def WriteMemory(plc, byte, bit, datatype, value):
    result = plc.read_area(Areas['MK'], 0, byte, datatype)
    if datatype == S7WLBit:
        set_bool(result, 0, bit, value)
    elif datatype == S7WLByte or datatype == S7WLWord:
        set_int(result, 0, value)
    elif datatype == S7WLReal:
        set_real(result, 0, value)
    elif datatype == S7WLDWord:
        set_dword(result, 0, value)
    plc.write_area(Areas["MK"], 0, byte, result)


def ReadMemory(plc, byte, bit, datatype):
    result = plc.read_area(Areas['MK'], 0, byte, datatype)
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


if __name__ == "__main__":
    plc = c.Client()
    plc.connect('192.168.0.1', 0, 1)
    print(plc.get_connected())
    time.sleep(2)
    WriteMemory(plc, 0, 0, S7WLBit, 1)
    print('Done')
    print(ReadMemory(plc, 100, 0, S7WLWord))