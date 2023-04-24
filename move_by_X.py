import pyvisa as visa
import time
import cv2
import sys
import usb.core
import usb.util
import numpy as np
import config_constants as cc

def moveX(x):
    
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

    print(x)

    #Use this section to move in pos x
    if x > 0:
        #alpha
        ta = abs(x/posA_speed)

        #C2 100
        #print(vi.query("*idn?"))
        print("Configuring C2")
        vi.write("c2:bswv frq,10") #set the frequency of channel 1
        vi.write("c2:bswv wvtp,ramp") #set the type of waveform
        vi.write("c2:bswv amp, %s" %voltage) #set the amplitude
        vi.write("c2:bswv sym, 100") #set the amplitude
        vi.write("c2:bswv duty,75") #duty cycle
        vi.write("c2:bswv dlay, 1") #brust delay for 1 second
        vi.write("c2:output on")
        time.sleep(ta)
        vi.write("c2:output off")
        time.sleep(2)

    #Use this section to move in neg x
    if x < 0:
        #-alpha
        ta = abs(x/negA_speed)

        #C2 0
        #print(vi.query("*idn?"))
        print("Configuring C2")
        vi.write("c2:bswv frq,10") #set the frequency of channel 1
        vi.write("c2:bswv wvtp,ramp") #set the type of waveform
        vi.write("c2:bswv amp, %s" %voltage) #set the amplitude
        vi.write("c2:bswv sym, 0") #set the amplitude
        vi.write("c2:bswv duty,75") #duty cycle
        vi.write("c2:bswv dlay, 1") #brust delay for 1 second
        vi.write("c2:output on")
        time.sleep(ta)
        vi.write("c2:output off")
        time.sleep(2)
