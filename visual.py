# Code is a modified version of 'Jose Julio @2009 "IMU_Razor9DOF.py"'
# This script needs VPhyton, pyserial and pywin modules

# First Install Python 2.6.4
# Install pywin from http://sourceforge.net/projects/pywin32/
# Install pyserial from http://sourceforge.net/projects/pyserial/files/
# Install Vphyton from http://vpython.org/contents/download_windows.html
#python 2.7

from visual import *
import serial
import string
import math
import serial

connected = False
port = '/dev/tty.usbserial-1420'
baud = 115200
g = 9.834

serial_port = serial.Serial(port, baud, timeout=0)

from time import time,sleep

deg2rad = 3.141592/180.0
#gennaro ser = serial.Serial(port='COM9',baudrate=115200,timeout=1)
# Main scene
scene=display(title="JB Robotics IMU")
scene.range=(1.2,1.2,1.2)
scene.forward = (1,0,-0.25)
scene.up=(0,0,1)

# Second scene (Roll, Pitch, Yaw)
scene2 = display(title='JB Robotics IMU',x=0, y=0, width=500, height=200,center=(0,0,0), background=(0,0,0))
scene2.range=(1,1,1)
scene.width=500
scene.y=200

scene2.select()
#Roll, Pitch, Yaw
cil_roll = cylinder(pos=(-0.4,0,0),axis=(0.2,0,0),radius=0.01,color=color.red)
cil_roll2 = cylinder(pos=(-0.4,0,0),axis=(-0.2,0,0),radius=0.01,color=color.red)
cil_pitch = cylinder(pos=(0.1,0,0),axis=(0.2,0,0),radius=0.01,color=color.green)
cil_pitch2 = cylinder(pos=(0.1,0,0),axis=(-0.2,0,0),radius=0.01,color=color.green)
arrow_course = arrow(pos=(0.6,0,0),color=color.cyan,axis=(-0.2,0,0), shaftwidth=0.02, fixedwidth=1)

#Roll,Pitch,Yaw labels
label(pos=(-0.4,0.3,0),text="Roll",box=0,opacity=0)
label(pos=(0.1,0.3,0),text="Pitch",box=0,opacity=0)
label(pos=(0.55,0.3,0),text="Yaw",box=0,opacity=0)
label(pos=(0.6,0.22,0),text="N",box=0,opacity=0,color=color.yellow)
label(pos=(0.6,-0.22,0),text="S",box=0,opacity=0,color=color.yellow)
label(pos=(0.38,0,0),text="W",box=0,opacity=0,color=color.yellow)
label(pos=(0.82,0,0),text="E",box=0,opacity=0,color=color.yellow)
label(pos=(0.75,0.15,0),height=7,text="NE",box=0,color=color.yellow)
label(pos=(0.45,0.15,0),height=7,text="NW",box=0,color=color.yellow)
label(pos=(0.75,-0.15,0),height=7,text="SE",box=0,color=color.yellow)
label(pos=(0.45,-0.15,0),height=7,text="SW",box=0,color=color.yellow)

L1 = label(pos=(-0.4,0.22,0),text="-",box=0,opacity=0)
L2 = label(pos=(0.1,0.22,0),text="-",box=0,opacity=0)
L3 = label(pos=(0.7,0.3,0),text="-",box=0,opacity=0)

# Main scene objects
scene.select()
# Reference axis (x,y,z)
arrow(color=color.green,axis=(1,0,0), shaftwidth=0.02, fixedwidth=1)
arrow(color=color.green,axis=(0,-1,0), shaftwidth=0.02 , fixedwidth=1)
arrow(color=color.green,axis=(0,0,-1), shaftwidth=0.02, fixedwidth=1)
# labels
label(pos=(0,0,0.8),text="JB Robotics IMU",box=0,opacity=0)
label(pos=(1,0,0),text="X",box=0,opacity=0)
label(pos=(0,-1,0),text="Y",box=0,opacity=0)
label(pos=(0,0,-1),text="Z",box=0,opacity=0)
# IMU object
platform = box(length=1, height=0.05, width=1, color=color.red)
p_line = box(length=1,height=0.08,width=0.1,color=color.yellow)
plat_arrow = arrow(color=color.green,axis=(1,0,0), shaftwidth=0.06, fixedwidth=1)


def converti (mbyte):
    if len(mbyte) ==0:
        return 0
    else:
        return ord(mbyte)


roll=0
pitch=0
yaw=0
counter = 0
while 1:

    line = 'RPY: 10 10 10' #ser.readline()
    line = line.replace("RPY: ","")
    words = string.split(line," ") # Fields split
    sleep(1)

    isU = serial_port.read()
    #print(isU)
    if isU == b'U': 
        isQ = serial_port.read()
        if isQ == b'Q':
            #print('found UQ')
            AxL = converti(serial_port.read())
            AxH = converti(serial_port.read())
            AyL = converti(serial_port.read())
            AyH = converti(serial_port.read())
            AzL = converti(serial_port.read())
            AzH = converti(serial_port.read())
            TL  = converti(serial_port.read())
            TH  = converti(serial_port.read())
            sum = converti(serial_port.read())
            ax =((AxH << 8)|AxL)/32768.0*16*g
            ay =((AyH << 8)|AyL)/32768.0*16*g
            az =((AzH << 8)|AzL)/32768.0*16*g
            T = ((TH << 8)|TL)/340+36.53
            Checksum  = 85 + 81  + AxH + AxL + AyH + AyL + AzH + AzL + TH + TL
            Lower = divmod(Checksum, 0x100) [1]
            #if sum == Lower:
            #    print( '%4.4f  %4.4f %4.4f ' % (ax,ay,az))

            isU = serial_port.read()
            isR = serial_port.read()
            if isR == b'R':
                WxL = converti(serial_port.read())
                WxH = converti(serial_port.read())
                WyL = converti(serial_port.read())
                WyH = converti(serial_port.read())
                WzL = converti(serial_port.read())
                WzH = converti(serial_port.read())
                TL  = converti(serial_port.read())
                TH  = converti(serial_port.read())
                sum = converti(serial_port.read())
                wx =((WxH << 8)|WxL)/32768.0*2000
                wy =((WyH << 8)|WyL)/32768.0*2000
                wz =((WzH << 8)|WzL)/32768.0*2000
                
                isU = serial_port.read()
                isS = serial_port.read()
                if isS == b'S':
                    RollL = converti(serial_port.read())
                    RollH = converti(serial_port.read())
                    PitchL = converti(serial_port.read())
                    PitchH = converti(serial_port.read())
                    YawL = converti(serial_port.read())
                    YawH = converti(serial_port.read())
                    TL  = converti(serial_port.read())
                    TH  = converti(serial_port.read())
                    sum = converti(serial_port.read())
                    Roll =((RollH << 8)|RollL)/32768.0*180
                    Pitch =((PitchH << 8)|PitchL)/32768.0*180
                    Yaw =((YawH << 8)|YawL)/32768.0*180
                    print( '%4.4f  %4.4f %4.4f ' % (Roll,Pitch,Yaw))
                    counter = counter + 1


                    if (counter % 1000) == 0:
                        try:
                            roll = float(Roll)*deg2rad
                            pitch = float(Pitch)*deg2rad
                            yaw = float(Yaw)*deg2rad
                        except:
                            print("Invalid line")
                        axis=(cos(pitch)*cos(yaw),-cos(pitch)*sin(yaw),sin(pitch))
                        up=(sin(roll)*sin(yaw)+cos(roll)*sin(pitch)*cos(yaw),sin(roll)*cos(yaw)-cos(roll)*sin(pitch)*sin(yaw),-cos(roll)*cos(pitch))
                        platform.axis=axis
                        platform.up=up
                        platform.length=1.0
                        platform.width=0.65
                        plat_arrow.axis=axis
                        plat_arrow.up=up
                        plat_arrow.length=0.8
                        p_line.axis=axis
                        p_line.up=up
                        cil_roll.axis=(0.2*cos(roll),0.2*sin(roll),0)
                        cil_roll2.axis=(-0.2*cos(roll),-0.2*sin(roll),0)
                        cil_pitch.axis=(0.2*cos(pitch),0.2*sin(pitch),0)
                        cil_pitch2.axis=(-0.2*cos(pitch),-0.2*sin(pitch),0)
                        arrow_course.axis=(0.2*sin(yaw),0.2*cos(yaw),0)

                        L1.text = str(float(Roll))
                        L2.text = str(float(Pitch))
                        L3.text = str(float(Yaw))
