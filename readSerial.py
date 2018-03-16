import threading
import serial

connected = False
port = '/dev/tty.usbserial-1410'
baud = 115200
g = 9.834

serial_port = serial.Serial(port, baud, timeout=0)

while(True):
    isU = serial_port.read()
    #print(isU)
    if isU == b'U': 
        isQ = serial_port.read()
        if isQ == b'Q':
            #print('found UQ')
            #AxLB = serial_port.read()
            #AxL = int.from_bytes(AxLB, byteorder='big') 
            AxL = int.from_bytes(serial_port.read(), byteorder='big')
            AxH = int.from_bytes(serial_port.read(), byteorder='big')
            AyL = int.from_bytes(serial_port.read(), byteorder='big')
            AyH = int.from_bytes(serial_port.read(), byteorder='big') 
            AzL = int.from_bytes(serial_port.read(), byteorder='big')
            AzH = int.from_bytes(serial_port.read(), byteorder='big') 
            TL  = int.from_bytes(serial_port.read(), byteorder='big') 
            TH  = int.from_bytes(serial_port.read(), byteorder='big') 
            sum = int.from_bytes(serial_port.read(), byteorder='big')
            ax =((AxH << 8)|AxL)/32768*16*g
            ay =((AyH << 8)|AyL)/32768*16*g
            az =((AzH << 8)|AzL)/32768*16*g
            T = ((TH << 8)|TL)/340+36.53
            Checksum  = 85 + 81  + AxH + AxL + AyH + AyL + AzH + AzL + TH + TL
            Lower = divmod(Checksum, 0x100) [1]
            #if sum == Lower:
            #    print( '%4.4f  %4.4f %4.4f ' % (ax,ay,az))

            isU = serial_port.read()
            isR = serial_port.read()
            if isR == b'R':
                WxL = int.from_bytes(serial_port.read(), byteorder='big') 
                WxH = int.from_bytes(serial_port.read(), byteorder='big') 
                WyL = int.from_bytes(serial_port.read(), byteorder='big')
                WyH = int.from_bytes(serial_port.read(), byteorder='big')
                WzL = int.from_bytes(serial_port.read(), byteorder='big')
                WzH = int.from_bytes(serial_port.read(), byteorder='big')
                TL  = int.from_bytes(serial_port.read(), byteorder='big')
                TH  = int.from_bytes(serial_port.read(), byteorder='big') 
                sum = int.from_bytes(serial_port.read(), byteorder='big')
                wx =((WxH << 8)|WxL)/32768*2000
                wy =((WyH << 8)|WyL)/32768*2000
                wz =((WzH << 8)|WzL)/32768*2000
                
                isU = serial_port.read()
                isS = serial_port.read()
                if isS == b'S':
                    RollL = int.from_bytes(serial_port.read(), byteorder='big')
                    RollH = int.from_bytes(serial_port.read(), byteorder='big')
                    PitchL = int.from_bytes(serial_port.read(), byteorder='big')
                    PitchH = int.from_bytes(serial_port.read(), byteorder='big')
                    YawL = int.from_bytes(serial_port.read(), byteorder='big')
                    YawH = int.from_bytes(serial_port.read(), byteorder='big') 
                    TL  = int.from_bytes(serial_port.read(), byteorder='big')
                    TH  = int.from_bytes(serial_port.read(), byteorder='big')
                    sum = int.from_bytes(serial_port.read(), byteorder='big')
                    Roll =((RollH << 8)|RollL)/32768*180
                    Pitch =((PitchH << 8)|PitchL)/32768*180
                    yaw =((YawH << 8)|YawL)/32768*180
                    print( '%4.4f  %4.4f %4.4f ' % (Roll,Pitch,yaw))


    #else:
        #print('not found')
