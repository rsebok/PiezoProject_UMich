#These functions are used to move the positioner for a certain amount of time at a certain voltage
#Input:distance to move 

#Last updated 05/09/2023 by RAS - simplified to have fewer inputs


import pyvisa as visa
import time
import cv2
import sys
import usb.core
import usb.util
import config_constants as cc

def move_posX(x):
    
    posX_speed = cc.speeds['posX']
    voltage = cc.voltage
        
    t = abs(x/posX_speed)
    
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    if voltage >=6:
        print('That voltage is too high!')
        return
    
    print('posX,',voltage,'Vpp,',"10 Hz,",t,'s')
        
    print("Configuring C1")
    vi.write("c1:bswv frq, 10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c1:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c1:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv sym, 0") #set the symmetry
    time.sleep(0.6)
    vi.write("c1:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c1:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c1:output on")
    time.sleep(t)
    vi.write("c1:output off")
    time.sleep(0.6)
    
    print('Move done.')

def move_posY(y):
    
    posY_speed = cc.speeds['posY']
    voltage = cc.voltage

    t = abs(y/posY_speed)    
    
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
        
    if voltage >=6:
        print('That voltage is too high!')
        return
        
    print('posY,',voltage,'Vpp,',"10 Hz,",t,'s')
    
    print("Configuring C2")
    vi.write("c2:bswv frq, 10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c2:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c2:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv sym, 100") #set the symmetry
    time.sleep(0.6)
    vi.write("c2:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c2:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c2:output on")
    time.sleep(t)
    vi.write("c2:output off")
    time.sleep(0.6)
    
    print('Move done.')

def move_negX(x):
    
    negX_speed = cc.speeds['negX']
    voltage = cc.voltage

    t = abs(x/negX_speed)
    
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
        
    
    if voltage >=6:
        print('That voltage is too high!')
        return
        
    print('negX,',voltage,'Vpp,',"10 Hz,",t,'s')
 
    print("Configuring C1")
    vi.write("c1:bswv frq,10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c1:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c1:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv sym, 100") #set the symmetry
    time.sleep(0.6)
    vi.write("c1:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c1:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c1:output on")
    time.sleep(t)
    vi.write("c1:output off")
    time.sleep(0.6)
    
    print('Move done.')
    
def move_negY(y):
    
    negY_speed = cc.speeds['negY']
    voltage = cc.voltage

    t = abs(y/negY_speed)
    
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
     
    
    if voltage >=6:
        print('That voltage is too high!')
        return
        
    print('negY,',voltage,'Vpp,',"10 Hz,",t,'s')
 
    print("Configuring C2")
    vi.write("c2:bswv frq,10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c2:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c2:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv sym, 0") #set the symmetry
    time.sleep(0.6)
    vi.write("c2:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c2:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c2:output on")
    time.sleep(t)
    vi.write("c2:output off")
    time.sleep(0.6)

    print('Move done.')
