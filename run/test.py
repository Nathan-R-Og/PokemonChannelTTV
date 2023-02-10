import ctypes
from mem_edit import Process
import struct

pointer = 0x7ff70b1f7e40

addrs = {
    "cursorX": 0x547280,
    "cursorY": 0x547284,
    "zoom": 0x2CBB34,
    "changes": 0x2C4F58,
}
vars = {
    "cursorX": 0.0,
    "cursorY": 0.0,
    "zoom": 0,
    "changes": 0,
}

byteLimit = {
    "1": 128,
    "2": 32768,
    "4": 2147483648,
}
def numToHex(input, limit, header = False):
    base = hex(input)
    if base[0] == "-":
        #neg
        sub = ""
        while len(sub) < limit * 2:
            sub += "F"
        sub = hex(int(sub, 16) + 1)
        base = hex(int(sub, 16) + int(base, 16))
    end = base.replace("0x", "").upper()
    while len(end) < limit * 2:
        end = "0" + end
    if header:
        end = "0x" + end
    return end
def floatToHex(input, header = False):
    result = hex(struct.unpack('<I', struct.pack('<f', input))[0]).replace("0x", "").upper()
    while len(result) < 4 * 2:
        result = "0" + result
    if header:
        result = "0x" + result
    return result
def hexToNum(input, limit, signed):
    inter = int(input, 16)
    maxer = byteLimit[str(limit)] * 2
    halfer = byteLimit[str(limit)]
    if signed:
        while inter >= halfer:
            inter -= maxer
        while inter < -halfer:
            inter += maxer
    else:
        while inter >= maxer:
            inter -= maxer
        while inter < -maxer:
            inter += maxer
    return inter
def hexToFloat(input):
    return struct.unpack('!f', bytes.fromhex(input))[0]
def bigEndianIze(input, size):
    return int.to_bytes(input, length=size, byteorder="little")
def bytesToString(bye):
    beyotch = ""
    for each in bye:
        beyotch += hex(each).replace("0x", "", 1).zfill(2)
    return beyotch


with Process.open_process(Process.get_pid_by_name('Dolphin.exe')) as p:
    #get the base pointer    
    pointer = p.read_memory(pointer, ctypes.c_uint64()).value
    pointer = list(bigEndianIze(pointer, 8))
    pointer.reverse()
    pointer = int(bytesToString(pointer), 16)
    


    #add to the offset
    for key in list(addrs.keys()):
        addrs[key] += pointer

    while 1:
        u1 = p.read_memory(addrs["cursorX"], ctypes.c_ulong()).value
        u1 = list(bigEndianIze(u1, 4))
        vars["cursorX"] = hexToFloat(bytesToString(u1))
        
        u1 = p.read_memory(addrs["cursorY"], ctypes.c_ulong()).value
        u1 = list(bigEndianIze(u1, 4))
        vars["cursorY"] = hexToFloat(bytesToString(u1))
        
        u1 = p.read_memory(addrs["zoom"], ctypes.c_ushort()).value
        u1 = list(bigEndianIze(u1, 2))
        vars["zoom"] = hexToNum(bytesToString(u1), 2, False)

        u1 = p.read_memory(addrs["changes"], ctypes.c_ulong()).value
        u1 = list(bigEndianIze(u1, 4))
        vars["changes"] = hexToNum(bytesToString(u1), 4, False)



        print(vars)




        #u2 = floatToHex(2.762418032)
        #u2 = bytes.fromhex(u2)
        #u2 = int.from_bytes(u2, "little")
        #"4030CB75"
        #p.write_memory(j, ctypes.c_int16(u2))



        #p.write_memory(addrs[0], ctypes.c_ulong(num + 1))