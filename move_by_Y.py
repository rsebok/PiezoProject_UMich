import pyvisa as visa
import time
import cv2
import sys
import usb.core
import usb.util
import numpy as np
import config_constants as cc

def moveY(y):
    
    rm = visa.ResourceManager()
    li = rm.list_resources()
    print(li)
    vi = rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    vi.read_termination = '\r'
    vi.write_termination = '\r'
    
    posA_speed = cc.speeds['negX']
    posB_speed = cc.speeds['negY']
    negB_speed = cc.speeds['posY']
    negA_speed = cc.speeds['posX']
    voltage = cc.voltage

    print(y)

    #Use this section to move in pos y
    if y > 0:
        #beta
        tb = abs(y/posB_speed)

        #C1 100
        #print(vi.query("*idn?"))
        print("Configuring C1")
        vi.write("c1:bswv frq,10") #set the frequency of channel 1
        vi.write("c1:bswv wvtp,ramp") #set the type of waveform
        vi.write("c1:bswv amp, %s" %voltage) #set the amplitude
        vi.write("c1:bswv sym, 100") #set the amplitude
        vi.write("c1:bswv duty,75") #duty cycle
        vi.write("c1:bswv dlay, 1") #brust delay for 1 second
        vi.write("c1:output on")
        time.sleep(tb)
        vi.write("c1:output off")
        time.sleep(2)

    #Use this section to move in neg y
    if y < 0:
        #-beta
        tb = abs(y/negB_speed)

        #C1 0
        #print(vi.query("*idn?"))
        print("Configuring C1")
        vi.write("c1:bswv frq,10") #set the frequency of channel 1
        vi.write("c1:bswv wvtp,ramp") #set the type of waveform
        vi.write("c1:bswv amp, %s" %voltage) #set the amplitude
        vi.write("c1:bswv sym, 0") #set the amplitude
        vi.write("c1:bswv duty,75") #duty cycle
        vi.write("c1:bswv dlay, 1") #brust delay for 1 second
        vi.write("c1:output on")
        time.sleep(tb)
        vi.write("c1:output off")
        time.sleep(2)
        
