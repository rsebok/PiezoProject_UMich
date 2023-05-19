#These functions are used to move the positioner EVEN SMALLER distances by changing the frequency and voltage to the smallest usable values
#Input: distance to move

#Last updated 05/18/2023 by RAS - moved the numbers into the config folder

import pyvisa as visa
import time
import cv2
import sys
import usb.core
import usb.util
import config_constants as cc

negX_speed = cc.speeds['negX']
negY_speed = cc.speeds['negY']
posY_speed = cc.speeds['posY']
posX_speed = cc.speeds['posX']
newt = cc.micro_time
freq = cc.micro_freq
voltage_posX = cc.micro_voltage_posX
voltage_negX = cc.micro_voltage_negX
voltage_posY = cc.micro_voltage_posY
voltage_negY = cc.micro_voltage_negY

def micromove_posX(x):
    #Use this section to move in pos x
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')

    print('posX,',voltage_posX,'Vpp,',freq,"Hz,",newt,'s')

    print("Configuring C1")
    vi.write("c1:bswv frq, %s" %freq) #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c1:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c1:bswv amp, %s" %voltage_posX) #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv sym, 0") #set the symmetry
    time.sleep(0.6)
    vi.write("c1:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c1:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c1:output on")
    time.sleep(newt)
    vi.write("c1:output off")
    time.sleep(1)

    print('Micro move done.')
    
def micromove_negX(x):
    #Use this section to move in neg x
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')

    print('negX,',voltage_negX,'Vpp,',freq,"Hz,",newt,'s')

    print("Configuring C1")
    vi.write("c1:bswv frq, %s" %freq) #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c1:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c1:bswv amp, %s" %voltage_negX) #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv sym, 100") #set the symmetry
    time.sleep(0.6)
    vi.write("c1:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c1:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c1:output on")
    time.sleep(newt)
    vi.write("c1:output off")
    time.sleep(1)

    print('Micro move done.')

def micromove_negY(y):
    #Use this section to move in neg y
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')

    print('negY,',voltage_negY,'Vpp,',freq,"Hz,",newt,'s')

    print("Configuring C2")
    vi.write("c2:bswv frq, %s" %freq) #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c2:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c2:bswv amp, %s" %voltage_negY) #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv sym, 0") #set the symmetry
    time.sleep(0.6)
    vi.write("c2:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c2:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c2:output on")
    time.sleep(newt)
    vi.write("c2:output off")
    time.sleep(1)

    print('Micro move done.')

def micromove_posY(y):
    #Use this section to move in pos y
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    

    print('posY,',voltage_posY,'Vpp,',freq,"Hz,",newt,'s')

    print("Configuring C2")
    vi.write("c2:bswv frq, %s" %freq) #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c2:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c2:bswv amp, %s" %voltage_posY) #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv sym, 100") #set the symmetry
    time.sleep(0.6)
    vi.write("c2:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c2:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c2:output on")
    time.sleep(newt)
    vi.write("c2:output off")
    time.sleep(1)

    print('Micro move done.')

        
