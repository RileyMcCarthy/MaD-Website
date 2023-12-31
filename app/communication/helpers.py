import ctypes

def convert_to_bytes(st):
    buffer = ctypes.create_string_buffer(ctypes.sizeof(st))
    ctypes.memmove(buffer, ctypes.addressof(st), ctypes.sizeof(st))
    return buffer.raw

def structEq(comp, other):
    return convert_to_bytes(comp) == convert_to_bytes(other)

def crc8(data, length):
    crc = 0
    for i in range(length):
        inbyte = data[i]
        for j in range(8):
            mix = (crc ^ inbyte) & 0x01
            crc >>= 1
            if mix:
                crc ^= 0x8C
            inbyte >>= 1
    return crc